--!strict
-- MapController.client.luau
-- Sistema de Mapa Calibrado de Rosewood (Project Zomboid Build 42)
-- Tecla [M], Seguimiento en tiempo real con rotación de brújula, Zoom con rueda y Arrastre (Pan)
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local player = Players.LocalPlayer
local pgui = player:WaitForChild("PlayerGui")

local mapGui = Instance.new("ScreenGui")
mapGui.Name = "PZ_MapGui"
mapGui.ResetOnSpawn = false
mapGui.DisplayOrder = 100
mapGui.Parent = pgui

-- Ventana Principal del Mapa
local mainFrame = Instance.new("Frame")
mainFrame.Name = "MainFrame"
mainFrame.Size = UDim2.new(0, 760, 0, 580)
mainFrame.Position = UDim2.new(0.5, -380, 0.5, -290)
mainFrame.BackgroundColor3 = Color3.fromRGB(22, 22, 25)
mainFrame.BackgroundTransparency = 0.05
mainFrame.BorderSizePixel = 0
mainFrame.Visible = false
mainFrame.Parent = mapGui

local mainCorner = Instance.new("UICorner")
mainCorner.CornerRadius = UDim.new(0, 8)
mainCorner.Parent = mainFrame

local mainStroke = Instance.new("UIStroke")
mainStroke.Color = Color3.fromRGB(85, 80, 70)
mainStroke.Thickness = 2.5
mainStroke.Parent = mainFrame

-- Barra Superior
local topBar = Instance.new("Frame")
topBar.Size = UDim2.new(1, 0, 0, 42)
topBar.BackgroundColor3 = Color3.fromRGB(34, 32, 30)
topBar.BorderSizePixel = 0
topBar.Parent = mainFrame

local topBarCorner = Instance.new("UICorner")
topBarCorner.CornerRadius = UDim.new(0, 8)
topBarCorner.Parent = topBar

local titleLabel = Instance.new("TextLabel")
titleLabel.Size = UDim2.new(1, -120, 1, 0)
titleLabel.Position = UDim2.new(0, 16, 0, 0)
titleLabel.BackgroundTransparency = 1
titleLabel.Font = Enum.Font.GothamBold
titleLabel.Text = "KNOX COUNTY - ROSEWOOD, KY [MAPA TOPOGRÁFICO DE SUPERVIVENCIA]"
titleLabel.TextColor3 = Color3.fromRGB(225, 190, 115)
titleLabel.TextSize = 13
titleLabel.TextXAlignment = Enum.TextXAlignment.Left
titleLabel.Parent = topBar

local closeBtn = Instance.new("TextButton")
closeBtn.Size = UDim2.new(0, 30, 0, 30)
closeBtn.Position = UDim2.new(1, -38, 0, 6)
closeBtn.BackgroundColor3 = Color3.fromRGB(150, 45, 45)
closeBtn.Font = Enum.Font.GothamBold
closeBtn.Text = "X"
closeBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
closeBtn.TextSize = 13
closeBtn.Parent = topBar
local cbCorner = Instance.new("UICorner")
cbCorner.CornerRadius = UDim.new(0, 6)
cbCorner.Parent = closeBtn

-- Contenedor de Recorte del Mapa
local mapContainer = Instance.new("Frame")
mapContainer.Name = "MapContainer"
mapContainer.Size = UDim2.new(1, -24, 1, -84)
mapContainer.Position = UDim2.new(0, 12, 0, 48)
mapContainer.BackgroundColor3 = Color3.fromRGB(15, 15, 17)
mapContainer.ClipsDescendants = true
mapContainer.BorderSizePixel = 0
mapContainer.Parent = mainFrame

local mcCorner = Instance.new("UICorner")
mcCorner.CornerRadius = UDim.new(0, 6)
mcCorner.Parent = mapContainer

-- Imagen del Mapa con soporte de Zoom y Pan
local currentZoom = 1.0
local panOffset = Vector2.zero
local isDragging = false
local dragStartMouse = Vector2.zero
local dragStartPan = Vector2.zero

local mapImage = Instance.new("ImageLabel")
mapImage.Name = "MapImage"
mapImage.Size = UDim2.new(1, 0, 1, 0)
mapImage.Position = UDim2.new(0, 0, 0, 0)
mapImage.Image = "rbxasset://pz42/rosewood_map.png"
mapImage.ScaleType = Enum.ScaleType.Fit
mapImage.BackgroundTransparency = 1
mapImage.Parent = mapContainer

-- Calibración de Coordenadas de Rosewood
local MAP_MIN_X = -187.5
local MAP_MAX_X = 187.5
local MAP_MIN_Z = -262.5
local MAP_MAX_Z = 262.5
local MAP_W = MAP_MAX_X - MAP_MIN_X
local MAP_H = MAP_MAX_Z - MAP_MIN_Z

local function worldToMap(wx: number, wz: number): (number, number)
	local u = math.clamp((wx - MAP_MIN_X) / MAP_W, 0.02, 0.98)
	local v = math.clamp((wz - MAP_MIN_Z) / MAP_H, 0.02, 0.98)
	return u, v
end

-- Puntos de Interés (POIs) Calibrados
local POIS = {
	{ name = "Comisaría de Policía", x = -81.7, z = 123.8, col = Color3.fromRGB(65, 125, 235) },
	{ name = "Estación de Bomberos", x = 111.8, z = 198.8, col = Color3.fromRGB(225, 65, 45) },
	{ name = "Banco de Rosewood", x = -57.3, z = -218.2, col = Color3.fromRGB(235, 195, 55) },
	{ name = "Cafetería / Panadería", x = -138.0, z = -224.9, col = Color3.fromRGB(205, 135, 85) },
	{ name = "Librería y Comercio", x = 80.2, z = -165.0, col = Color3.fromRGB(135, 85, 215) },
	{ name = "Bar de Rosewood", x = -75.7, z = -28.4, col = Color3.fromRGB(215, 105, 35) },
	{ name = "Oficinas y Supermercado", x = -56.2, z = -104.2, col = Color3.fromRGB(95, 185, 95) },
	{ name = "Restaurante Chino", x = 70.2, z = 13.6, col = Color3.fromRGB(235, 85, 125) },
}

for _, poi in ipairs(POIS) do
	local u, v = worldToMap(poi.x, poi.z)
	local pin = Instance.new("Frame")
	pin.Name = "POI_" .. poi.name
	pin.Size = UDim2.new(0, 10, 0, 10)
	pin.AnchorPoint = Vector2.new(0.5, 0.5)
	pin.Position = UDim2.new(u, 0, v, 0)
	pin.BackgroundColor3 = poi.col
	pin.BorderSizePixel = 0
	pin.Parent = mapImage

	local cr = Instance.new("UICorner")
	cr.CornerRadius = UDim.new(1, 0)
	cr.Parent = pin
	local strk = Instance.new("UIStroke")
	strk.Color = Color3.fromRGB(255, 255, 255)
	strk.Thickness = 1
	strk.Parent = pin

	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(0, 120, 0, 15)
	lbl.Position = UDim2.new(0.5, -60, 1, 2)
	lbl.BackgroundColor3 = Color3.fromRGB(20, 20, 22)
	lbl.BackgroundTransparency = 0.25
	lbl.Font = Enum.Font.GothamBold
	lbl.Text = poi.name
	lbl.TextColor3 = Color3.fromRGB(240, 240, 240)
	lbl.TextSize = 9
	lbl.Parent = pin
	local lcr = Instance.new("UICorner")
	lcr.CornerRadius = UDim.new(0, 4)
	lcr.Parent = lbl
end

-- Marcador del Superviviente con Flecha de Orientación
local playerMarker = Instance.new("Frame")
playerMarker.Name = "PlayerMarker"
playerMarker.Size = UDim2.new(0, 20, 0, 20)
playerMarker.AnchorPoint = Vector2.new(0.5, 0.5)
playerMarker.Position = UDim2.new(0.5, 0, 0.5, 0)
playerMarker.BackgroundColor3 = Color3.fromRGB(235, 45, 45)
playerMarker.ZIndex = 10
playerMarker.Parent = mapImage

local pmCorner = Instance.new("UICorner")
pmCorner.CornerRadius = UDim.new(1, 0)
pmCorner.Parent = playerMarker
local pmStroke = Instance.new("UIStroke")
pmStroke.Color = Color3.fromRGB(255, 255, 255)
pmStroke.Thickness = 2
pmStroke.Parent = playerMarker

local arrowLabel = Instance.new("TextLabel")
arrowLabel.Name = "HeadingArrow"
arrowLabel.Size = UDim2.new(1, 0, 1, 0)
arrowLabel.BackgroundTransparency = 1
arrowLabel.Font = Enum.Font.GothamBold
arrowLabel.Text = "▲"
arrowLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
arrowLabel.TextSize = 13
arrowLabel.Parent = playerMarker

local tagLabel = Instance.new("TextLabel")
tagLabel.Size = UDim2.new(0, 34, 0, 13)
tagLabel.Position = UDim2.new(0.5, -17, 1, 2)
tagLabel.BackgroundColor3 = Color3.fromRGB(235, 45, 45)
tagLabel.Font = Enum.Font.GothamBold
tagLabel.Text = "TÚ"
tagLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
tagLabel.TextSize = 9
tagLabel.Parent = playerMarker
local tagCorner = Instance.new("UICorner")
tagCorner.CornerRadius = UDim.new(0, 3)
tagCorner.Parent = tagLabel

-- Barra Inferior
local bottomBar = Instance.new("Frame")
bottomBar.Size = UDim2.new(1, -24, 0, 28)
bottomBar.Position = UDim2.new(0, 12, 1, -32)
bottomBar.BackgroundTransparency = 1
bottomBar.Parent = mainFrame

local coordText = Instance.new("TextLabel")
coordText.Size = UDim2.new(0.5, 0, 1, 0)
coordText.BackgroundTransparency = 1
coordText.Font = Enum.Font.GothamMedium
coordText.Text = "COORD: X 0.0 | Z 0.0"
coordText.TextColor3 = Color3.fromRGB(180, 180, 185)
coordText.TextSize = 11
coordText.TextXAlignment = Enum.TextXAlignment.Left
coordText.Parent = bottomBar

local guideText = Instance.new("TextLabel")
guideText.Size = UDim2.new(0.5, 0, 1, 0)
guideText.Position = UDim2.new(0.5, 0, 0, 0)
guideText.BackgroundTransparency = 1
guideText.Font = Enum.Font.Gotham
guideText.Text = "Rueda Ratón: Zoom | Arrastrar: Mover | [M]: Cerrar"
guideText.TextColor3 = Color3.fromRGB(225, 190, 115)
guideText.TextSize = 11
guideText.TextXAlignment = Enum.TextXAlignment.Right
guideText.Parent = bottomBar

-- Apertura / Cierre del Mapa
local isMapOpen = false
local function toggleMap()
	isMapOpen = not isMapOpen
	mainFrame.Visible = isMapOpen
end
closeBtn.MouseButton1Click:Connect(function()
	if isMapOpen then toggleMap() end
end)

UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end
	if input.KeyCode == Enum.KeyCode.M then
		toggleMap()
	elseif input.KeyCode == Enum.KeyCode.Escape and isMapOpen then
		toggleMap()
	end
end)

-- Zoom con la rueda del ratón dentro del mapa
mapContainer.InputChanged:Connect(function(input)
	if not isMapOpen then return end
	if input.UserInputType == Enum.UserInputType.MouseWheel then
		local newZoom = math.clamp(currentZoom + input.Position.Z * 0.25, 1.0, 3.2)
		currentZoom = newZoom
		mapImage.Size = UDim2.new(currentZoom, 0, currentZoom, 0)
	end
end)

-- Arrastre (Pan) con Clic Izquierdo sostenido
mapContainer.InputBegan:Connect(function(input)
	if not isMapOpen then return end
	if input.UserInputType == Enum.UserInputType.MouseButton1 then
		isDragging = true
		dragStartMouse = Vector2.new(input.Position.X, input.Position.Y)
		dragStartPan = panOffset
	end
end)

UserInputService.InputEnded:Connect(function(input)
	if input.UserInputType == Enum.UserInputType.MouseButton1 then
		isDragging = false
	end
end)

UserInputService.InputChanged:Connect(function(input)
	if isMapOpen and isDragging and input.UserInputType == Enum.UserInputType.MouseMovement then
		local currentMouse = Vector2.new(input.Position.X, input.Position.Y)
		local delta = currentMouse - dragStartMouse
		local maxPan = (currentZoom - 1.0) * 350.0
		panOffset = Vector2.new(
			math.clamp(dragStartPan.X + delta.X, -maxPan, maxPan),
			math.clamp(dragStartPan.Y + delta.Y, -maxPan, maxPan)
		)
		mapImage.Position = UDim2.new(0, panOffset.X, 0, panOffset.Y)
	end
end)

-- Actualización continua del Pin y la Brújula en tiempo real
RunService.RenderStepped:Connect(function()
	if not isMapOpen then return end
	local char = player.Character
	if not char then return end
	local hrp = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not hrp then return end

	local p = hrp.Position
	local u, v = worldToMap(p.X, p.Z)
	playerMarker.Position = UDim2.new(u, 0, v, 0)
	coordText.Text = string.format("SUPERVIVIENTE: X %5.1f | Z %5.1f", p.X, p.Z)

	-- Orientación de la flecha según la dirección de mirada del personaje
	local look = hrp.CFrame.LookVector
	local headingAngle = math.deg(math.atan2(look.X, -look.Z))
	playerMarker.Rotation = headingAngle
	tagLabel.Rotation = -headingAngle -- Mantener la etiqueta "TÚ" horizontal
end)
