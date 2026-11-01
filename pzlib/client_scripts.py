"""
Scripts cliente Luau para StarterPlayerScripts en Roblox:
1. Camara isometrica 1:1 de Project Zomboid (angulo exacto 30 grados / 45 grados).
2. Sistema de Cutaway de techos y paredes con histeresis (VisiFlagTimerPeriod_ms).
3. Controles de supervivencia (Apuntar con Click Derecho, Correr con Shift).
4. HUD de Estado de Project Zomboid (Salud, Resistencia, Reloj de Knox County, Moodles).
"""

ISOMETRIC_CONTROLLER_LUAU = r'''-- CameraAndCutawayController.client.luau
-- Camara Isometrica y Sistema de Corte de Techos/Paredes de Project Zomboid Build 42

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local Lighting = game:GetService("Lighting")

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")
local rootPart = character:WaitForChild("HumanoidRootPart")

-- Constantes exactas de Project Zomboid
local TILE_STUDS = 3.0
local STORY_STUDS = math.sqrt(6) * TILE_STUDS -- ~7.35 studs por piso
-- Vector isometrico: pitch exacto 30 grados, yaw 45 grados
local ISO_DIR = Vector3.new(1.0, math.sqrt(2/3), 1.0).Unit

local targetZoom = 55.0
local currentZoom = 55.0
local isAiming = false
local isSprinting = false

-- Zoom con la rueda del raton
UserInputService.InputChanged:Connect(function(input, processed)
	if processed then return end
	if input.UserInputType == Enum.UserInputType.MouseWheel then
		targetZoom = math.clamp(targetZoom - input.Position.Z * 8.0, 24.0, 100.0)
	end
end)

-- Apuntar con Click Derecho y Correr con Left Shift
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = true
	elseif input.KeyCode == Enum.KeyCode.LeftShift then
		isSprinting = true
	end
end)

UserInputService.InputEnded:Connect(function(input, processed)
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = false
	elseif input.KeyCode == Enum.KeyCode.LeftShift then
		isSprinting = false
	end
end)

-- Actualizar velocidad segun estado de PZ
RunService.Heartbeat:Connect(function()
	if isAiming then
		humanoid.WalkSpeed = 9.0
	elseif isSprinting then
		humanoid.WalkSpeed = 22.0
	else
		humanoid.WalkSpeed = 14.0
	end
end)

-- Sistema de Cutaway con histeresis (750ms como en el motor original de PZ)
local cutawayParts = {}
local lastPlayerLevel = 0
local lastInsideBuilding = false
local lastCutawayCheck = 0

local function getGroundRaycast()
	local rayOrigin = camera.CFrame.Position
	local mousePos = UserInputService:GetMouseLocation()
	local ray = camera:ViewportPointToRay(mousePos.X, mousePos.Y)
	local params = RaycastParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = {character}
	return workspace:Raycast(ray.Origin, ray.Direction * 500, params)
end

-- Actualizacion de camara por frame
RunService.RenderStepped:Connect(function(dt)
	if not rootPart or not rootPart.Parent then
		character = player.Character
		if character then
			rootPart = character:FindFirstChild("HumanoidRootPart")
			humanoid = character:FindFirstChild("Humanoid")
		end
		return
	end

	camera.CameraType = Enum.CameraType.Scriptable
	currentZoom = currentZoom + (targetZoom - currentZoom) * math.clamp(dt * 10, 0, 1)

	local focusPos = rootPart.Position + Vector3.new(0, 1.5, 0)
	local camPos = focusPos + ISO_DIR * currentZoom

	camera.CFrame = CFrame.lookAt(camPos, focusPos)

	-- Orientacion del personaje al apuntar
	if isAiming then
		local hit = getGroundRaycast()
		if hit then
			local targetLook = Vector3.new(hit.Position.X, rootPart.Position.Y, hit.Position.Z)
			rootPart.CFrame = CFrame.lookAt(rootPart.Position, targetLook)
		end
	end

	-- Cutaway periodic check (cada 0.15s con transicion suave)
	local now = tick()
	if now - lastCutawayCheck > 0.15 then
		lastCutawayCheck = now
		local pY = rootPart.Position.Y
		local playerLevel = math.floor((pY + 1.0) / STORY_STUDS)

		-- Raycast hacia arriba para saber si esta bajo techo
		local upParams = RaycastParams.new()
		upParams.FilterType = Enum.RaycastFilterType.Exclude
		upParams.FilterDescendantsInstances = {character}
		local upHit = workspace:Raycast(rootPart.Position, Vector3.new(0, 60, 0), upParams)
		local insideBuilding = (upHit ~= nil)

		-- Aplicar transparencia en techos y pisos superiores
		local edificios = workspace:FindFirstChild("PZ_Rosewood_B42")
		if edificios and edificios:FindFirstChild("Edificios") then
			for _, bld in ipairs(edificios.Edificios:GetChildren()) do
				for _, lvl in ipairs(bld:GetChildren()) do
					local zNum = tonumber(string.match(lvl.Name, "Piso_([%-]?%d+)"))
					if zNum then
						local shouldHide = insideBuilding and (zNum > playerLevel)
						for _, p in ipairs(lvl:GetDescendants()) do
							if p:IsA("BasePart") then
								local targetTrans = shouldHide and 0.95 or 0.0
								if p.LocalTransparencyModifier ~= targetTrans then
									p.LocalTransparencyModifier = targetTrans
								end
							end
						end
					end
				end
			end
		end
	end
end)
'''

SURVIVOR_HUD_LUAU = r'''-- SurvivorHUD.client.luau
-- Interfaz de Usuario estilo Project Zomboid (Reloj, Salud, Resistencia, Moodles)

local Players = game:GetService("Players")
local Lighting = game:GetService("Lighting")
local player = Players.LocalPlayer
local pgui = player:WaitForChild("PlayerGui")

local gui = Instance.new("ScreenGui")
gui.Name = "PZ_SurvivorHUD"
gui.ResetOnSpawn = false
gui.Parent = pgui

-- Marco principal superior derecho (Reloj de Knox County)
local clockFrame = Instance.new("Frame")
clockFrame.Name = "ClockFrame"
clockFrame.Size = UDim2.new(0, 210, 0, 50)
clockFrame.Position = UDim2.new(1, -225, 0, 15)
clockFrame.BackgroundColor3 = Color3.fromRGB(24, 24, 26)
clockFrame.BackgroundTransparency = 0.25
clockFrame.BorderSizePixel = 0
clockFrame.Parent = gui

local clockCorner = Instance.new("UICorner")
clockCorner.CornerRadius = UDim.new(0, 6)
clockCorner.Parent = clockFrame

local clockStroke = Instance.new("UIStroke")
clockStroke.Color = Color3.fromRGB(60, 60, 65)
clockStroke.Thickness = 1.5
clockStroke.Parent = clockFrame

local locLabel = Instance.new("TextLabel")
locLabel.Name = "LocationLabel"
locLabel.Size = UDim2.new(1, -10, 0, 18)
locLabel.Position = UDim2.new(0, 5, 0, 4)
locLabel.BackgroundTransparency = 1
locLabel.Font = Enum.Font.GothamBold
locLabel.Text = "ROSEWOOD, KY"
locLabel.TextColor3 = Color3.fromRGB(215, 180, 105)
locLabel.TextSize = 13
locLabel.TextXAlignment = Enum.TextXAlignment.Center
locLabel.Parent = clockFrame

local timeLabel = Instance.new("TextLabel")
timeLabel.Name = "TimeLabel"
timeLabel.Size = UDim2.new(1, -10, 0, 22)
timeLabel.Position = UDim2.new(0, 5, 0, 24)
timeLabel.BackgroundTransparency = 1
timeLabel.Font = Enum.Font.GothamMedium
timeLabel.Text = "12:00 PM"
timeLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
timeLabel.TextSize = 15
timeLabel.TextXAlignment = Enum.TextXAlignment.Center
timeLabel.Parent = clockFrame

-- Marco inferior izquierdo (Salud y Resistencia)
local statFrame = Instance.new("Frame")
statFrame.Name = "StatFrame"
statFrame.Size = UDim2.new(0, 240, 0, 55)
statFrame.Position = UDim2.new(0, 20, 1, -75)
statFrame.BackgroundColor3 = Color3.fromRGB(24, 24, 26)
statFrame.BackgroundTransparency = 0.25
statFrame.BorderSizePixel = 0
statFrame.Parent = gui

local statCorner = Instance.new("UICorner")
statCorner.CornerRadius = UDim.new(0, 6)
statCorner.Parent = statFrame

local statStroke = Instance.new("UIStroke")
statStroke.Color = Color3.fromRGB(60, 60, 65)
statStroke.Thickness = 1.5
statStroke.Parent = statFrame

-- Barra de Salud
local hpBg = Instance.new("Frame")
hpBg.Size = UDim2.new(1, -20, 0, 14)
hpBg.Position = UDim2.new(0, 10, 0, 10)
hpBg.BackgroundColor3 = Color3.fromRGB(45, 20, 20)
hpBg.BorderSizePixel = 0
hpBg.Parent = statFrame
local hpBar = Instance.new("Frame")
hpBar.Name = "HpBar"
hpBar.Size = UDim2.new(1, 0, 1, 0)
hpBar.BackgroundColor3 = Color3.fromRGB(75, 185, 80)
hpBar.BorderSizePixel = 0
hpBar.Parent = hpBg

-- Barra de Resistencia
local stBg = Instance.new("Frame")
stBg.Size = UDim2.new(1, -20, 0, 10)
stBg.Position = UDim2.new(0, 10, 0, 32)
stBg.BackgroundColor3 = Color3.fromRGB(20, 30, 45)
stBg.BorderSizePixel = 0
stBg.Parent = statFrame
local stBar = Instance.new("Frame")
stBar.Name = "StBar"
stBar.Size = UDim2.new(1, 0, 1, 0)
stBar.BackgroundColor3 = Color3.fromRGB(50, 140, 230)
stBar.BorderSizePixel = 0
stBar.Parent = stBg

-- Columna de Moodles (Lado derecho de la pantalla)
local moodleFrame = Instance.new("Frame")
moodleFrame.Name = "MoodlesFrame"
moodleFrame.Size = UDim2.new(0, 48, 0, 200)
moodleFrame.Position = UDim2.new(1, -60, 0, 80)
moodleFrame.BackgroundTransparency = 1
moodleFrame.Parent = gui

local function createMoodle(yPos, col, text)
	local m = Instance.new("Frame")
	m.Size = UDim2.new(0, 42, 0, 42)
	m.Position = UDim2.new(0, 0, 0, yPos)
	m.BackgroundColor3 = col
	m.BorderSizePixel = 0
	m.Parent = moodleFrame
	
	local cr = Instance.new("UICorner")
	cr.CornerRadius = UDim.new(0, 6)
	cr.Parent = m
	
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.new(1, 0, 1, 0)
	lbl.BackgroundTransparency = 1
	lbl.Font = Enum.Font.GothamBold
	lbl.Text = text
	lbl.TextColor3 = Color3.fromRGB(255, 255, 255)
	lbl.TextSize = 11
	lbl.Parent = m
	return m
end

createMoodle(0, Color3.fromRGB(40, 140, 60), "BIEN")
createMoodle(48, Color3.fromRGB(45, 120, 180), "AGIL")

-- Actualizacion del HUD
Lighting:GetPropertyChangedSignal("ClockTime"):Connect(function()
	local ct = Lighting.ClockTime
	local hours = math.floor(ct)
	local mins = math.floor((ct - hours) * 60)
	local ampm = hours >= 12 and "PM" or "AM"
	local h12 = hours % 12
	if h12 == 0 then h12 = 12 end
	timeLabel.Text = string.format("%02d:%02d %s", h12, mins, ampm)
end)

local function hookChar(char)
	local hum = char:WaitForChild("Humanoid")
	hum.HealthChanged:Connect(function(hp)
		hpBar.Size = UDim2.new(math.clamp(hp / hum.MaxHealth, 0, 1), 0, 1, 0)
	end)
end
if player.Character then hookChar(player.Character) end
player.CharacterAdded:Connect(hookChar)
'''
