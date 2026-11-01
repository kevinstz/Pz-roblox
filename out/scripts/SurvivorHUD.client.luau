--!strict
-- SurvivorHUD.client.luau
-- MÓDULOS 5, 6 & 7: Inventario Doble [I], Panel de Salud Multipestaña [H] y Moodles Dinámicos de PZ Build 42
local Players = game:GetService("Players")
local Lighting = game:GetService("Lighting")
local UserInputService = game:GetService("UserInputService")
local TweenService = game:GetService("TweenService")
local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local player = Players.LocalPlayer
local pgui = player:WaitForChild("PlayerGui")

local hudGui = Instance.new("ScreenGui")
hudGui.Name = "PZ_SurvivorHUD"
hudGui.ResetOnSpawn = false
hudGui.DisplayOrder = 10
hudGui.Parent = pgui

-- RemoteEvents
local remotes = ReplicatedStorage:WaitForChild("PZ_Remotes", 10) :: Folder
local medicalRemote = remotes:WaitForChild("PZ_Medical", 10) :: RemoteEvent

-- Sonido de Latido de Corazón (Pánico)
local heartbeatSound = Instance.new("Sound")
heartbeatSound.Name = "HeartbeatSound"
heartbeatSound.SoundId = "rbxasset://sounds/electronicpingshort.wav"
heartbeatSound.Volume = 0.7
heartbeatSound.Looped = true
heartbeatSound.Parent = hudGui

--------------------------------------------------------------------------------
-- ESTADO MÉDICO, ESTADÍSTICAS Y HABILIDADES (MÓDULO 6 & 7)
--------------------------------------------------------------------------------
type BodyPartHealth = {
	name: string,
	status: string, -- "Sano", "Rasguño", "Laceración", "Mordido"
	isBleeding: boolean,
	isBandaged: boolean,
	infectionChance: number,
}

local bodyParts: { [string]: BodyPartHealth } = {
	Cabeza = { name = "Cabeza", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	Cuello = { name = "Cuello", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	Torso = { name = "Torso", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	BrazoIzq = { name = "Brazo Izquierdo", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	BrazoDer = { name = "Brazo Derecho", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	PiernaIzq = { name = "Pierna Izquierda", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
	PiernaDer = { name = "Pierna Derecha", status = "Sano", isBleeding = false, isBandaged = false, infectionChance = 0 },
}

local skills = {
	Carpinteria = { name = "Carpintería", lvl = 2, xp = 140, maxXp = 300 },
	ArmasContundentes = { name = "Armas Contundentes", lvl = 3, xp = 220, maxXp = 400 },
	Punteria = { name = "Puntería", lvl = 1, xp = 85, maxXp = 200 },
	Sigilo = { name = "Sigilo", lvl = 2, xp = 160, maxXp = 300 },
	PrimerosAuxilios = { name = "Primeros Auxilios", lvl = 1, xp = 50, maxXp = 200 },
}

local stats = {
	health = 100.0,
	stamina = 100.0,
	hunger = 10.0,  -- 0 (Lleno) a 100 (Hambriento)
	thirst = 10.0,  -- 0 (Hidratado) a 100 (Sediento)
	panic = 0.0,    -- 0 a 100
	maxWeight = 15.0,
	equippedSlot = 1,
	pistolAmmo = 15,
	daysSurvived = 1,
	calories = 2200,
}

type ItemData = { name: string, weight: number, icon: string, desc: string, category: string, count: number }

local playerInventory: { ItemData } = {
	{ name = "Bate con clavos", weight = 2.0, icon = "🏏", desc = "Arma contundente cuerpo a cuerpo.", category = "Armas", count = 1 },
	{ name = "Pistola 9mm", weight = 1.2, icon = "🔫", desc = "Pistola semiautomática de 9mm.", category = "Armas", count = 1 },
	{ name = "Caja de Balas 9mm", weight = 0.6, icon = "📦", desc = "30 balas de 9mm.", category = "Munición", count = 2 },
	{ name = "Vendaje Estéril", weight = 0.15, icon = "🩹", desc = "Detiene hemorragias al vendar.", category = "Medicina", count = 3 },
	{ name = "Tela Rasgada", weight = 0.1, icon = "🧵", desc = "Vendaje improvisado.", category = "Medicina", count = 2 },
	{ name = "Botella de Agua", weight = 0.8, icon = "💧", desc = "Agua fresca de Kentucky.", category = "Bebida", count = 1 },
	{ name = "Lata de Frijoles", weight = 0.4, icon = "🥫", desc = "Alimento imperecedero.", category = "Comida", count = 2 },
	{ name = "Analgésicos", weight = 0.1, icon = "💊", desc = "Alivia el dolor corporal.", category = "Medicina", count = 1 },
	{ name = "Alcohol desinfectante", weight = 0.3, icon = "🧪", desc = "Desinfecta heridas y telas.", category = "Medicina", count = 1 },
}

local currentLootContainerName = "Suelo"
local currentLootItems: { ItemData } = {}

local function calcTotalWeight(items: { ItemData }): number
	local w = 0
	for _, it in ipairs(items) do w += it.weight * it.count end
	return math.round(w * 10) / 10
end

-- Listener de drenaje de stamina desde combate
local staminaDrainEvent = Instance.new("BindableEvent")
staminaDrainEvent.Name = "PZ_HUD_DrainStamina"
staminaDrainEvent.Parent = ReplicatedStorage
staminaDrainEvent.Event:Connect(function(amount: number)
	stats.stamina = math.max(0, stats.stamina - amount)
end)

--------------------------------------------------------------------------------
-- 1. RELOJ DIGITAL DE PULSERA (ROSEWOOD, KY - 09 JUL 1993)
--------------------------------------------------------------------------------
local watchFrame = Instance.new("Frame")
watchFrame.Name = "WatchFrame"
watchFrame.Size = UDim2.new(0, 220, 0, 62)
watchFrame.Position = UDim2.new(1, -235, 0, 16)
watchFrame.BackgroundColor3 = Color3.fromRGB(24, 24, 28)
watchFrame.BackgroundTransparency = 0.15
watchFrame.BorderSizePixel = 0
watchFrame.Parent = hudGui

local wCorner = Instance.new("UICorner")
wCorner.CornerRadius = UDim.new(0, 8)
wCorner.Parent = watchFrame

local wStroke = Instance.new("UIStroke")
wStroke.Color = Color3.fromRGB(70, 65, 55)
wStroke.Thickness = 1.5
wStroke.Parent = watchFrame

local wLoc = Instance.new("TextLabel")
wLoc.Size = UDim2.new(1, -12, 0, 15)
wLoc.Position = UDim2.new(0, 10, 0, 4)
wLoc.BackgroundTransparency = 1
wLoc.Font = Enum.Font.GothamBold
wLoc.Text = "ROSEWOOD, KY"
wLoc.TextColor3 = Color3.fromRGB(225, 190, 115)
wLoc.TextSize = 12
wLoc.TextXAlignment = Enum.TextXAlignment.Left
wLoc.Parent = watchFrame

local wTime = Instance.new("TextLabel")
wTime.Size = UDim2.new(1, -12, 0, 22)
wTime.Position = UDim2.new(0, 10, 0, 19)
wTime.BackgroundTransparency = 1
wTime.Font = Enum.Font.RobotoMono
wTime.Text = "09:00 AM"
wTime.TextColor3 = Color3.fromRGB(250, 250, 250)
wTime.TextSize = 18
wTime.TextXAlignment = Enum.TextXAlignment.Left
wTime.Parent = watchFrame

local wDate = Instance.new("TextLabel")
wDate.Size = UDim2.new(1, -12, 0, 15)
wDate.Position = UDim2.new(0, 10, 0, 42)
wDate.BackgroundTransparency = 1
wDate.Font = Enum.Font.Gotham
wDate.Text = "09 JUL 1993 | 24°C Despejado"
wDate.TextColor3 = Color3.fromRGB(165, 165, 175)
wDate.TextSize = 11
wDate.TextXAlignment = Enum.TextXAlignment.Left
wDate.Parent = watchFrame

--------------------------------------------------------------------------------
-- 2. MOODLES DINÁMICOS CON NIVELES DE GRAVEDAD Y TOOLTIPS (MÓDULO 7)
--------------------------------------------------------------------------------
local moodlesContainer = Instance.new("Frame")
moodlesContainer.Name = "MoodlesContainer"
moodlesContainer.Size = UDim2.new(0, 52, 0, 360)
moodlesContainer.Position = UDim2.new(1, -64, 0, 95)
moodlesContainer.BackgroundTransparency = 1
moodlesContainer.Parent = hudGui

local moodleListLayout = Instance.new("UIListLayout")
moodleListLayout.FillDirection = Enum.FillDirection.Vertical
moodleListLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
moodleListLayout.SortOrder = Enum.SortOrder.LayoutOrder
moodleListLayout.Padding = UDim.new(0, 8)
moodleListLayout.Parent = moodlesContainer

local tooltipLabel = Instance.new("TextLabel")
tooltipLabel.Name = "MoodleTooltip"
tooltipLabel.Size = UDim2.new(0, 200, 0, 36)
tooltipLabel.BackgroundColor3 = Color3.fromRGB(20, 20, 22)
tooltipLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
tooltipLabel.Font = Enum.Font.GothamMedium
tooltipLabel.TextSize = 12
tooltipLabel.Visible = false
tooltipLabel.BorderSizePixel = 0
tooltipLabel.ZIndex = 50
tooltipLabel.Parent = hudGui

local ttCorner = Instance.new("UICorner")
ttCorner.CornerRadius = UDim.new(0, 6)
ttCorner.Parent = tooltipLabel

local moodleButtons: { [string]: { btn: ImageButton, stroke: UIStroke, getTooltip: () -> string } } = {}

local function createMoodle(key: string, iconEmoji: string, getTooltipFunc: () -> string): ImageButton
	local btn = Instance.new("ImageButton")
	btn.Name = "Moodle_" .. key
	btn.Size = UDim2.new(0, 44, 0, 44)
	btn.BackgroundColor3 = Color3.fromRGB(28, 28, 32)
	btn.AutoButtonColor = false
	btn.Visible = false
	btn.Parent = moodlesContainer

	local bCorner = Instance.new("UICorner")
	bCorner.CornerRadius = UDim.new(1, 0)
	bCorner.Parent = btn

	local bStroke = Instance.new("UIStroke")
	bStroke.Thickness = 2.5
	bStroke.Color = Color3.fromRGB(220, 50, 50)
	bStroke.Parent = btn

	local emojiLbl = Instance.new("TextLabel")
	emojiLbl.Size = UDim2.new(1, 0, 1, 0)
	emojiLbl.BackgroundTransparency = 1
	emojiLbl.Text = iconEmoji
	emojiLbl.TextSize = 22
	emojiLbl.Parent = btn

	btn.MouseEnter:Connect(function()
		tooltipLabel.Text = getTooltipFunc()
		tooltipLabel.Position = UDim2.new(1, -270, 0, btn.AbsolutePosition.Y)
		tooltipLabel.Visible = true
	end)

	btn.MouseLeave:Connect(function()
		tooltipLabel.Visible = false
	end)

	moodleButtons[key] = { btn = btn, stroke = bStroke, getTooltip = getTooltipFunc }
	return btn
end

createMoodle("Bleeding", "🩸", function() return "Hemorragia: ¡Pierdes sangre por heridas abiertas!" end)
createMoodle("Panic", "😱", function() return string.format("Pánico (%d%%): Zombis cerca. Precisión reducida.", math.round(stats.panic)) end)
createMoodle("Exhaustion", "💨", function() return string.format("Agotado (%d%% Stamina): Reduce velocidad y daño.", math.round(stats.stamina)) end)
createMoodle("Hunger", "🍗", function() return string.format("Hambre (%d%%): Necesitas alimentarte.", math.round(stats.hunger)) end)
createMoodle("Thirst", "💧", function() return string.format("Sed (%d%%): Deshidratación activa.", math.round(stats.thirst)) end)
createMoodle("HeavyLoad", "🎒", function() return string.format("Sobrecarga (%.1f / %.1f kg): Reduce velocidad.", calcTotalWeight(playerInventory), stats.maxWeight) end)

--------------------------------------------------------------------------------
-- 3. HOTBAR FUNCIONAL (1, 2, 3) ABAJO AL CENTRO
--------------------------------------------------------------------------------
local hotbarFrame = Instance.new("Frame")
hotbarFrame.Name = "HotbarFrame"
hotbarFrame.Size = UDim2.new(0, 240, 0, 68)
hotbarFrame.Position = UDim2.new(0.5, -120, 1, -84)
hotbarFrame.BackgroundColor3 = Color3.fromRGB(22, 22, 25)
hotbarFrame.BackgroundTransparency = 0.2
hotbarFrame.BorderSizePixel = 0
hotbarFrame.Parent = hudGui

local hbCorner = Instance.new("UICorner")
hbCorner.CornerRadius = UDim.new(0, 10)
hbCorner.Parent = hotbarFrame

local hbLayout = Instance.new("UIListLayout")
hbLayout.FillDirection = Enum.FillDirection.Horizontal
hbLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
hbLayout.VerticalAlignment = Enum.VerticalAlignment.Center
hbLayout.Padding = UDim.new(0, 10)
hbLayout.Parent = hotbarFrame

local hotbarSlots: { [number]: { frame: ImageButton, label: TextLabel, subText: TextLabel, stroke: UIStroke } } = {}

local slotConfigs = {
	{ slot = 1, key = "1", name = "Bate", icon = "🏏" },
	{ slot = 2, key = "2", name = "Pistola", icon = "🔫" },
	{ slot = 3, key = "3", name = "Vendaje", icon = "🩹" },
}

for _, cfg in ipairs(slotConfigs) do
	local sBtn = Instance.new("ImageButton")
	sBtn.Name = "Slot_" .. cfg.slot
	sBtn.Size = UDim2.new(0, 64, 0, 54)
	sBtn.BackgroundColor3 = Color3.fromRGB(34, 34, 38)
	sBtn.AutoButtonColor = true
	sBtn.Parent = hotbarFrame

	local sCorner = Instance.new("UICorner")
	sCorner.CornerRadius = UDim.new(0, 6)
	sCorner.Parent = sBtn

	local sStroke = Instance.new("UIStroke")
	sStroke.Thickness = if cfg.slot == 1 then 2.0 else 1.0
	sStroke.Color = if cfg.slot == 1 then Color3.fromRGB(225, 190, 115) else Color3.fromRGB(65, 65, 70)
	sStroke.Parent = sBtn

	local kLabel = Instance.new("TextLabel")
	kLabel.Size = UDim2.new(0, 16, 0, 14)
	kLabel.Position = UDim2.new(0, 4, 0, 2)
	kLabel.BackgroundTransparency = 1
	kLabel.Font = Enum.Font.RobotoMono
	kLabel.Text = cfg.key
	kLabel.TextColor3 = Color3.fromRGB(180, 180, 180)
	kLabel.TextSize = 11
	kLabel.Parent = sBtn

	local iconLbl = Instance.new("TextLabel")
	iconLbl.Size = UDim2.new(1, 0, 0, 26)
	iconLbl.Position = UDim2.new(0, 0, 0, 12)
	iconLbl.BackgroundTransparency = 1
	iconLbl.Text = cfg.icon
	iconLbl.TextSize = 20
	iconLbl.Parent = sBtn

	local subLbl = Instance.new("TextLabel")
	subLbl.Size = UDim2.new(1, 0, 0, 14)
	subLbl.Position = UDim2.new(0, 0, 1, -16)
	subLbl.BackgroundTransparency = 1
	subLbl.Font = Enum.Font.GothamMedium
	subLbl.Text = if cfg.slot == 2 then "15/15" else cfg.name
	subLbl.TextColor3 = Color3.fromRGB(210, 210, 210)
	subLbl.TextSize = 10
	subLbl.Parent = sBtn

	sBtn.MouseButton1Click:Connect(function()
		stats.equippedSlot = cfg.slot
		for s, data in pairs(hotbarSlots) do
			data.stroke.Color = if s == cfg.slot then Color3.fromRGB(225, 190, 115) else Color3.fromRGB(65, 65, 70)
			data.stroke.Thickness = if s == cfg.slot then 2.0 else 1.0
		end
		local hudEv = ReplicatedStorage:FindFirstChild("PZ_HUD_UpdateSlot") :: BindableEvent?
		if hudEv then hudEv:Fire(cfg.slot, stats.pistolAmmo) end
	end)

	hotbarSlots[cfg.slot] = { frame = sBtn, label = iconLbl, subText = subLbl, stroke = sStroke }
end

local hudUpdateEvent = Instance.new("BindableEvent")
hudUpdateEvent.Name = "PZ_HUD_UpdateSlot"
hudUpdateEvent.Parent = ReplicatedStorage

hudUpdateEvent.Event:Connect(function(slot: number, ammo: number)
	stats.equippedSlot = slot
	stats.pistolAmmo = ammo
	for s, data in pairs(hotbarSlots) do
		data.stroke.Color = if s == slot then Color3.fromRGB(225, 190, 115) else Color3.fromRGB(65, 65, 70)
		data.stroke.Thickness = if s == slot then 2.0 else 1.0
	end
	if hotbarSlots[2] then
		hotbarSlots[2].subText.Text = ammo .. "/15"
	end
end)

--------------------------------------------------------------------------------
-- 4. BOTONES LATERALES: CORAZÓN [H] Y MOCHILA [I]
--------------------------------------------------------------------------------
local leftToolbar = Instance.new("Frame")
leftToolbar.Name = "LeftToolbar"
leftToolbar.Size = UDim2.new(0, 48, 0, 108)
leftToolbar.Position = UDim2.new(0, 16, 0.5, -54)
leftToolbar.BackgroundColor3 = Color3.fromRGB(24, 24, 28)
leftToolbar.BackgroundTransparency = 0.25
leftToolbar.BorderSizePixel = 0
leftToolbar.Parent = hudGui

local ltCorner = Instance.new("UICorner")
ltCorner.CornerRadius = UDim.new(0, 8)
ltCorner.Parent = leftToolbar

local heartBtn = Instance.new("TextButton")
heartBtn.Name = "HeartButton"
heartBtn.Size = UDim2.new(0, 40, 0, 44)
heartBtn.Position = UDim2.new(0, 4, 0, 6)
heartBtn.BackgroundTransparency = 1
heartBtn.Text = "❤️"
heartBtn.TextSize = 24
heartBtn.Parent = leftToolbar

local invBtn = Instance.new("TextButton")
invBtn.Name = "InvButton"
invBtn.Size = UDim2.new(0, 40, 0, 44)
invBtn.Position = UDim2.new(0, 4, 0, 56)
invBtn.BackgroundTransparency = 1
invBtn.Text = "🎒"
invBtn.TextSize = 24
invBtn.Parent = leftToolbar

--------------------------------------------------------------------------------
-- 5. PANEL DE SALUD MULTIPESTAÑA [H] (MÓDULO 6)
--------------------------------------------------------------------------------
local medicalWindow = Instance.new("Frame")
medicalWindow.Name = "MedicalWindow"
medicalWindow.Size = UDim2.new(0, 380, 0, 440)
medicalWindow.Position = UDim2.new(0, 72, 0.5, -220)
medicalWindow.BackgroundColor3 = Color3.fromRGB(24, 24, 28)
medicalWindow.BorderSizePixel = 0
medicalWindow.Visible = false
medicalWindow.Parent = hudGui

local mwCorner = Instance.new("UICorner")
mwCorner.CornerRadius = UDim.new(0, 10)
mwCorner.Parent = medicalWindow

local mwStroke = Instance.new("UIStroke")
mwStroke.Color = Color3.fromRGB(75, 70, 60)
mwStroke.Thickness = 1.5
mwStroke.Parent = medicalWindow

-- Pestañas superiores: [ Salud ], [ Info / Peso ], [ Habilidades ]
local tabContainer = Instance.new("Frame")
tabContainer.Size = UDim2.new(1, -20, 0, 32)
tabContainer.Position = UDim2.new(0, 10, 0, 10)
tabContainer.BackgroundTransparency = 1
tabContainer.Parent = medicalWindow

local tabLayout = Instance.new("UIListLayout")
tabLayout.FillDirection = Enum.FillDirection.Horizontal
tabLayout.Padding = UDim.new(0, 6)
tabLayout.Parent = tabContainer

local currentMedicalTab = "Salud"
local tabButtons: { [string]: TextButton } = {}
local tabContents: { [string]: Frame } = {}

local function createTabBtn(tabName: string)
	local tBtn = Instance.new("TextButton")
	tBtn.Name = "Tab_" .. tabName
	tBtn.Size = UDim2.new(0, 110, 1, 0)
	tBtn.BackgroundColor3 = if tabName == "Salud" then Color3.fromRGB(45, 45, 52) else Color3.fromRGB(30, 30, 34)
	tBtn.Font = Enum.Font.GothamBold
	tBtn.Text = tabName
	tBtn.TextColor3 = if tabName == "Salud" then Color3.fromRGB(225, 190, 115) else Color3.fromRGB(170, 170, 180)
	tBtn.TextSize = 11
	tBtn.Parent = tabContainer

	local tc = Instance.new("UICorner")
	tc.CornerRadius = UDim.new(0, 6)
	tc.Parent = tBtn

	tabButtons[tabName] = tBtn
end

createTabBtn("Salud")
createTabBtn("Info / Peso")
createTabBtn("Habilidades")

-- Contenido Tab 1: Salud
local saludTabFrame = Instance.new("Frame")
saludTabFrame.Name = "SaludTab"
saludTabFrame.Size = UDim2.new(1, -20, 1, -54)
saludTabFrame.Position = UDim2.new(0, 10, 0, 48)
saludTabFrame.BackgroundTransparency = 1
saludTabFrame.Parent = medicalWindow
tabContents["Salud"] = saludTabFrame

local bodyDiagram = Instance.new("Frame")
bodyDiagram.Name = "BodyDiagram"
bodyDiagram.Size = UDim2.new(0, 140, 0, 270)
bodyDiagram.Position = UDim2.new(0, 10, 0, 10)
bodyDiagram.BackgroundColor3 = Color3.fromRGB(16, 16, 18)
bodyDiagram.BorderSizePixel = 0
bodyDiagram.Parent = saludTabFrame

local bdCorner = Instance.new("UICorner")
bdCorner.CornerRadius = UDim.new(0, 8)
bdCorner.Parent = bodyDiagram

local limbLayout = {
	{ key = "Cabeza", name = "Cabeza", x = 50, y = 10, w = 40, h = 34 },
	{ key = "Cuello", name = "Cuello", x = 58, y = 46, w = 24, h = 14 },
	{ key = "Torso", name = "Torso", x = 40, y = 62, w = 60, h = 82 },
	{ key = "BrazoIzq", name = "Brazo Izq", x = 10, y = 66, w = 26, h = 80 },
	{ key = "BrazoDer", name = "Brazo Der", x = 104, y = 66, w = 26, h = 80 },
	{ key = "PiernaIzq", name = "Pierna Izq", x = 40, y = 148, w = 28, h = 110 },
	{ key = "PiernaDer", name = "Pierna Der", x = 72, y = 148, w = 28, h = 110 },
}

local limbButtons: { [string]: TextButton } = {}
local selectedLimbKey = "BrazoIzq"

local medicalInfoLabel = Instance.new("TextLabel")
medicalInfoLabel.Size = UDim2.new(0, 185, 0, 185)
medicalInfoLabel.Position = UDim2.new(0, 165, 0, 10)
medicalInfoLabel.BackgroundColor3 = Color3.fromRGB(18, 18, 20)
medicalInfoLabel.TextColor3 = Color3.fromRGB(240, 240, 240)
medicalInfoLabel.Font = Enum.Font.Gotham
medicalInfoLabel.TextSize = 12
medicalInfoLabel.TextXAlignment = Enum.TextXAlignment.Left
medicalInfoLabel.TextYAlignment = Enum.TextYAlignment.Top
medicalInfoLabel.Parent = saludTabFrame

local miCorner = Instance.new("UICorner")
miCorner.CornerRadius = UDim.new(0, 6)
miCorner.Parent = medicalInfoLabel

local applyBandageBtn = Instance.new("TextButton")
applyBandageBtn.Size = UDim2.new(0, 185, 0, 36)
applyBandageBtn.Position = UDim2.new(0, 165, 0, 205)
applyBandageBtn.BackgroundColor3 = Color3.fromRGB(50, 110, 60)
applyBandageBtn.Font = Enum.Font.GothamBold
applyBandageBtn.Text = "🩹 Aplicar Vendaje"
applyBandageBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
applyBandageBtn.TextSize = 12
applyBandageBtn.Parent = saludTabFrame

local abCorner = Instance.new("UICorner")
abCorner.CornerRadius = UDim.new(0, 6)
abCorner.Parent = applyBandageBtn

local function updateMedicalUI()
	for key, btn in pairs(limbButtons) do
		local data = bodyParts[key]
		if data.isBandaged then
			btn.BackgroundColor3 = Color3.fromRGB(80, 140, 190) -- Azul vendado
		elseif data.isBleeding or data.status == "Mordido" then
			btn.BackgroundColor3 = Color3.fromRGB(220, 50, 50) -- Rojo crítico
		elseif data.status == "Laceración" or data.status == "Rasguño" then
			btn.BackgroundColor3 = Color3.fromRGB(230, 130, 40) -- Naranja herida
		else
			btn.BackgroundColor3 = Color3.fromRGB(60, 160, 80) -- Verde sano
		end
	end

	local sel = bodyParts[selectedLimbKey]
	if sel then
		local text = string.format("EXTREMIDAD: %s\n\nEstado: %s\nRiesgo Infección: %d%%\nHemorragia: %s\nVendaje: %s\n\nSalud Global: %d%%",
			sel.name,
			sel.status,
			sel.infectionChance,
			if sel.isBleeding then "¡SÍ (Activa)!" else "No",
			if sel.isBandaged then "Vendado estéril" else "Sin vendaje",
			math.round(stats.health)
		)
		medicalInfoLabel.Text = text
	end
end

for _, lCfg in ipairs(limbLayout) do
	local lBtn = Instance.new("TextButton")
	lBtn.Name = "Limb_" .. lCfg.key
	lBtn.Size = UDim2.new(0, lCfg.w, 0, lCfg.h)
	lBtn.Position = UDim2.new(0, lCfg.x, 0, lCfg.y)
	lBtn.BackgroundColor3 = Color3.fromRGB(60, 160, 80)
	lBtn.Text = ""
	lBtn.Parent = bodyDiagram

	local lbCorner = Instance.new("UICorner")
	lbCorner.CornerRadius = UDim.new(0, 4)
	lbCorner.Parent = lBtn

	lBtn.MouseButton1Click:Connect(function()
		selectedLimbKey = lCfg.key
		updateMedicalUI()
	end)

	limbButtons[lCfg.key] = lBtn
end

applyBandageBtn.MouseButton1Click:Connect(function()
	local sel = bodyParts[selectedLimbKey]
	if sel and (sel.status ~= "Sano" or sel.isBleeding) then
		local foundIndex = -1
		for idx, it in ipairs(playerInventory) do
			if (it.name:find("Vendaje") or it.name:find("Tela Rasgada")) and it.count > 0 then
				foundIndex = idx
				break
			end
		end

		if foundIndex ~= -1 then
			playerInventory[foundIndex].count -= 1
			if playerInventory[foundIndex].count <= 0 then
				table.remove(playerInventory, foundIndex)
			end
			sel.isBandaged = true
			sel.isBleeding = false
			stats.health = math.min(stats.health + 18, 100)
			skills.PrimerosAuxilios.xp = math.min(skills.PrimerosAuxilios.maxXp, skills.PrimerosAuxilios.xp + 25)
			updateMedicalUI()
		end
	end
end)

-- Contenido Tab 2: Info / Peso
local infoTabFrame = Instance.new("Frame")
infoTabFrame.Name = "InfoTab"
infoTabFrame.Size = UDim2.new(1, -20, 1, -54)
infoTabFrame.Position = UDim2.new(0, 10, 0, 48)
infoTabFrame.BackgroundTransparency = 1
infoTabFrame.Visible = false
infoTabFrame.Parent = medicalWindow
tabContents["Info / Peso"] = infoTabFrame

local infoStatsLabel = Instance.new("TextLabel")
infoStatsLabel.Size = UDim2.new(1, 0, 1, 0)
infoStatsLabel.BackgroundColor3 = Color3.fromRGB(18, 18, 20)
infoStatsLabel.TextColor3 = Color3.fromRGB(230, 230, 230)
infoStatsLabel.Font = Enum.Font.RobotoMono
infoStatsLabel.TextSize = 13
infoStatsLabel.TextXAlignment = Enum.TextXAlignment.Left
infoStatsLabel.TextYAlignment = Enum.TextYAlignment.Top
infoStatsLabel.Parent = infoTabFrame

local function updateInfoTab()
	infoStatsLabel.Text = string.format([[
  === REGISTRO DEL SUPERVIVIENTE ===

  Ubicación: Rosewood, Knox County, KY
  Fecha: 09 de Julio de 1993
  Días Sobrevividos: %d

  Peso Actual: %.1f kg (Capacidad: %.1f kg)
  Calorías: %d kcal
  Stamina: %d%%
  Hambre: %d%%
  Sed: %d%%
  Pánico: %d%%

  Infección Zombi: %s
]],
		stats.daysSurvived,
		calcTotalWeight(playerInventory), stats.maxWeight,
		stats.calories,
		math.round(stats.stamina),
		math.round(stats.hunger),
		math.round(stats.thirst),
		math.round(stats.panic),
		if bodyParts.Cabeza.status == "Mordido" or bodyParts.Torso.status == "Mordido" then "¡POSITIVO (Fatal)!" else "Negativo"
	)
end

-- Contenido Tab 3: Habilidades
local skillsTabFrame = Instance.new("Frame")
skillsTabFrame.Name = "SkillsTab"
skillsTabFrame.Size = UDim2.new(1, -20, 1, -54)
skillsTabFrame.Position = UDim2.new(0, 10, 0, 48)
skillsTabFrame.BackgroundTransparency = 1
skillsTabFrame.Visible = false
skillsTabFrame.Parent = medicalWindow
tabContents["Habilidades"] = skillsTabFrame

local skillsLayout = Instance.new("UIListLayout")
skillsLayout.Padding = UDim.new(0, 8)
skillsLayout.Parent = skillsTabFrame

local function updateSkillsTab()
	for _, c in ipairs(skillsTabFrame:GetChildren()) do
		if c:IsA("Frame") then c:Destroy() end
	end
	for _, sk in pairs(skills) do
		local row = Instance.new("Frame")
		row.Size = UDim2.new(1, 0, 0, 48)
		row.BackgroundColor3 = Color3.fromRGB(28, 28, 33)
		row.Parent = skillsTabFrame

		local rc = Instance.new("UICorner")
		rc.CornerRadius = UDim.new(0, 6)
		rc.Parent = row

		local nameLbl = Instance.new("TextLabel")
		nameLbl.Size = UDim2.new(1, -12, 0, 20)
		nameLbl.Position = UDim2.new(0, 8, 0, 4)
		nameLbl.BackgroundTransparency = 1
		nameLbl.Font = Enum.Font.GothamBold
		nameLbl.Text = string.format("%s (Nivel %d)", sk.name, sk.lvl)
		nameLbl.TextColor3 = Color3.fromRGB(225, 190, 115)
		nameLbl.TextSize = 12
		nameLbl.TextXAlignment = Enum.TextXAlignment.Left
		nameLbl.Parent = row

		local barBg = Instance.new("Frame")
		barBg.Size = UDim2.new(1, -16, 0, 12)
		barBg.Position = UDim2.new(0, 8, 0, 26)
		barBg.BackgroundColor3 = Color3.fromRGB(15, 15, 18)
		barBg.Parent = row

		local barFill = Instance.new("Frame")
		barFill.Size = UDim2.new(math.clamp(sk.xp / sk.maxXp, 0, 1), 0, 1, 0)
		barFill.BackgroundColor3 = Color3.fromRGB(50, 140, 70)
		barFill.BorderSizePixel = 0
		barFill.Parent = barBg
	end
end

for name, btn in pairs(tabButtons) do
	btn.MouseButton1Click:Connect(function()
		currentMedicalTab = name
		for n, b in pairs(tabButtons) do
			b.BackgroundColor3 = if n == name then Color3.fromRGB(45, 45, 52) else Color3.fromRGB(30, 30, 34)
			b.TextColor3 = if n == name then Color3.fromRGB(225, 190, 115) else Color3.fromRGB(170, 170, 180)
		end
		for n, frame in pairs(tabContents) do
			frame.Visible = (n == name)
		end
		if name == "Salud" then updateMedicalUI() end
		if name == "Info / Peso" then updateInfoTab() end
		if name == "Habilidades" then updateSkillsTab() end
	end)
end

--------------------------------------------------------------------------------
-- 6. SISTEMA DE INVENTARIO DOBLE Y SAQUEO DE CONTENEDORES (MÓDULO 5)
--------------------------------------------------------------------------------
local doubleInventoryWindow = Instance.new("Frame")
doubleInventoryWindow.Name = "DoubleInventoryWindow"
doubleInventoryWindow.Size = UDim2.new(0, 700, 0, 460)
doubleInventoryWindow.Position = UDim2.new(0.5, -350, 0.5, -230)
doubleInventoryWindow.BackgroundColor3 = Color3.fromRGB(22, 22, 26)
doubleInventoryWindow.BorderSizePixel = 0
doubleInventoryWindow.Visible = false
doubleInventoryWindow.Parent = hudGui

local diCorner = Instance.new("UICorner")
diCorner.CornerRadius = UDim.new(0, 10)
diCorner.Parent = doubleInventoryWindow

local diStroke = Instance.new("UIStroke")
diStroke.Color = Color3.fromRGB(75, 70, 60)
diStroke.Thickness = 1.5
diStroke.Parent = doubleInventoryWindow

-- Panel Izquierdo: Inventario del Jugador
local playerInvPanel = Instance.new("Frame")
playerInvPanel.Name = "PlayerInvPanel"
playerInvPanel.Size = UDim2.new(0.5, -12, 1, -20)
playerInvPanel.Position = UDim2.new(0, 10, 0, 10)
playerInvPanel.BackgroundColor3 = Color3.fromRGB(28, 28, 33)
playerInvPanel.BorderSizePixel = 0
playerInvPanel.Parent = doubleInventoryWindow

local pipCorner = Instance.new("UICorner")
pipCorner.CornerRadius = UDim.new(0, 8)
pipCorner.Parent = playerInvPanel

local pipTitle = Instance.new("TextLabel")
pipTitle.Size = UDim2.new(1, -16, 0, 26)
pipTitle.Position = UDim2.new(0, 10, 0, 6)
pipTitle.BackgroundTransparency = 1
pipTitle.Font = Enum.Font.RobotoMono
pipTitle.Text = "INVENTARIO - Peso: 0.0 / 15.0"
pipTitle.TextColor3 = Color3.fromRGB(225, 190, 115)
pipTitle.TextSize = 12
pipTitle.TextXAlignment = Enum.TextXAlignment.Left
pipTitle.Parent = playerInvPanel

local pipScroll = Instance.new("ScrollingFrame")
pipScroll.Size = UDim2.new(1, -12, 1, -44)
pipScroll.Position = UDim2.new(0, 6, 0, 36)
pipScroll.BackgroundTransparency = 1
pipScroll.ScrollBarThickness = 5
pipScroll.CanvasSize = UDim2.new(0, 0, 2, 0)
pipScroll.Parent = playerInvPanel

local pipLayout = Instance.new("UIListLayout")
pipLayout.Padding = UDim.new(0, 4)
pipLayout.Parent = pipScroll

-- Panel Derecho: Botín Cercano
local lootPanel = Instance.new("Frame")
lootPanel.Name = "LootPanel"
lootPanel.Size = UDim2.new(0.5, -12, 1, -20)
lootPanel.Position = UDim2.new(0.5, 2, 0, 10)
lootPanel.BackgroundColor3 = Color3.fromRGB(28, 28, 33)
lootPanel.BorderSizePixel = 0
lootPanel.Parent = doubleInventoryWindow

local lpCorner = Instance.new("UICorner")
lpCorner.CornerRadius = UDim.new(0, 8)
lpCorner.Parent = lootPanel

local lpTitle = Instance.new("TextLabel")
lpTitle.Size = UDim2.new(1, -110, 0, 26)
lpTitle.Position = UDim2.new(0, 10, 0, 6)
lpTitle.BackgroundTransparency = 1
lpTitle.Font = Enum.Font.RobotoMono
lpTitle.Text = "BOTÍN CERCANO - Suelo"
lpTitle.TextColor3 = Color3.fromRGB(150, 190, 235)
lpTitle.TextSize = 12
lpTitle.TextXAlignment = Enum.TextXAlignment.Left
lpTitle.Parent = lootPanel

local lootAllBtn = Instance.new("TextButton")
lootAllBtn.Size = UDim2.new(0, 95, 0, 24)
lootAllBtn.Position = UDim2.new(1, -102, 0, 7)
lootAllBtn.BackgroundColor3 = Color3.fromRGB(45, 95, 155)
lootAllBtn.Font = Enum.Font.GothamBold
lootAllBtn.Text = "Tomar Todo"
lootAllBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
lootAllBtn.TextSize = 11
lootAllBtn.Parent = lootPanel

local labCorner = Instance.new("UICorner")
labCorner.CornerRadius = UDim.new(0, 5)
labCorner.Parent = lootAllBtn

local lpScroll = Instance.new("ScrollingFrame")
lpScroll.Size = UDim2.new(1, -12, 1, -44)
lpScroll.Position = UDim2.new(0, 6, 0, 36)
lpScroll.BackgroundTransparency = 1
lpScroll.ScrollBarThickness = 5
lpScroll.CanvasSize = UDim2.new(0, 0, 2, 0)
lpScroll.Parent = lootPanel

local lpLayout = Instance.new("UIListLayout")
lpLayout.Padding = UDim.new(0, 4)
lpLayout.Parent = lpScroll

-- Renderizado de Inventario y Botín
local function renderInventories()
	for _, c in ipairs(pipScroll:GetChildren()) do
		if c:IsA("Frame") or c:IsA("TextButton") then c:Destroy() end
	end
	for _, c in ipairs(lpScroll:GetChildren()) do
		if c:IsA("Frame") or c:IsA("TextButton") then c:Destroy() end
	end

	local curW = calcTotalWeight(playerInventory)
	pipTitle.Text = string.format("INVENTARIO - Peso: %.1f / %.1f", curW, stats.maxWeight)
	lpTitle.Text = "BOTÍN: " .. currentLootContainerName

	-- Renderizar Inventario con Menú Contextual
	for idx, it in ipairs(playerInventory) do
		local row = Instance.new("Frame")
		row.Size = UDim2.new(1, -4, 0, 34)
		row.BackgroundColor3 = Color3.fromRGB(36, 36, 42)
		row.BorderSizePixel = 0
		row.Parent = pipScroll

		local rCorner = Instance.new("UICorner")
		rCorner.CornerRadius = UDim.new(0, 5)
		rCorner.Parent = row

		local iconLbl = Instance.new("TextLabel")
		iconLbl.Size = UDim2.new(0, 24, 1, 0)
		iconLbl.Position = UDim2.new(0, 4, 0, 0)
		iconLbl.BackgroundTransparency = 1
		iconLbl.Text = it.icon
		iconLbl.TextSize = 16
		iconLbl.Parent = row

		local nameLbl = Instance.new("TextLabel")
		nameLbl.Size = UDim2.new(0, 140, 1, 0)
		nameLbl.Position = UDim2.new(0, 30, 0, 0)
		nameLbl.BackgroundTransparency = 1
		nameLbl.Font = Enum.Font.SourceSansBold
		nameLbl.Text = it.name .. (if it.count > 1 then " x" .. it.count else "")
		nameLbl.TextColor3 = Color3.fromRGB(240, 240, 240)
		nameLbl.TextSize = 13
		nameLbl.TextXAlignment = Enum.TextXAlignment.Left
		nameLbl.Parent = row

		-- Botones Contextuales [Usar / Equipar], [Soltar]
		local actionBtn = Instance.new("TextButton")
		actionBtn.Size = UDim2.new(0, 68, 0, 22)
		actionBtn.Position = UDim2.new(1, -125, 0, 6)
		actionBtn.BackgroundColor3 = Color3.fromRGB(50, 95, 60)
		actionBtn.Font = Enum.Font.SourceSansBold
		actionBtn.Text = if it.category == "Armas" then "Equipar" elseif it.category == "Comida" or it.category == "Bebida" then "Consumir" else "Usar"
		actionBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
		actionBtn.TextSize = 11
		actionBtn.Parent = row

		local ac = Instance.new("UICorner")
		ac.CornerRadius = UDim.new(0, 4)
		ac.Parent = actionBtn

		actionBtn.MouseButton1Click:Connect(function()
			if it.category == "Comida" then
				stats.hunger = math.max(0, stats.hunger - 35)
				it.count -= 1
				if it.count <= 0 then table.remove(playerInventory, idx) end
				renderInventories()
			elseif it.category == "Bebida" then
				stats.thirst = math.max(0, stats.thirst - 50)
				it.count -= 1
				if it.count <= 0 then table.remove(playerInventory, idx) end
				renderInventories()
			elseif it.category == "Medicina" then
				bodyParts.BrazoIzq.isBandaged = true
				bodyParts.BrazoIzq.isBleeding = false
				it.count -= 1
				if it.count <= 0 then table.remove(playerInventory, idx) end
				renderInventories()
			elseif it.category == "Armas" then
				local slot = if it.name:find("Bate") then 1 else 2
				local hudEv = ReplicatedStorage:FindFirstChild("PZ_HUD_UpdateSlot") :: BindableEvent?
				if hudEv then hudEv:Fire(slot, stats.pistolAmmo) end
			end
		end)

		local dropBtn = Instance.new("TextButton")
		dropBtn.Size = UDim2.new(0, 48, 0, 22)
		dropBtn.Position = UDim2.new(1, -52, 0, 6)
		dropBtn.BackgroundColor3 = Color3.fromRGB(110, 45, 45)
		dropBtn.Font = Enum.Font.SourceSansBold
		dropBtn.Text = "Soltar"
		dropBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
		dropBtn.TextSize = 11
		dropBtn.Parent = row

		local dc = Instance.new("UICorner")
		dc.CornerRadius = UDim.new(0, 4)
		dc.Parent = dropBtn

		dropBtn.MouseButton1Click:Connect(function()
			table.insert(currentLootItems, { name = it.name, weight = it.weight, icon = it.icon, desc = it.desc, category = it.category, count = 1 })
			it.count -= 1
			if it.count <= 0 then table.remove(playerInventory, idx) end
			renderInventories()
		end)
	end

	-- Renderizar Botín Cercano
	for idx, it in ipairs(currentLootItems) do
		local row = Instance.new("Frame")
		row.Size = UDim2.new(1, -4, 0, 34)
		row.BackgroundColor3 = Color3.fromRGB(36, 40, 48)
		row.BorderSizePixel = 0
		row.Parent = lpScroll

		local rCorner = Instance.new("UICorner")
		rCorner.CornerRadius = UDim.new(0, 5)
		rCorner.Parent = row

		local iconLbl = Instance.new("TextLabel")
		iconLbl.Size = UDim2.new(0, 24, 1, 0)
		iconLbl.Position = UDim2.new(0, 4, 0, 0)
		iconLbl.BackgroundTransparency = 1
		iconLbl.Text = it.icon
		iconLbl.TextSize = 16
		iconLbl.Parent = row

		local nameLbl = Instance.new("TextLabel")
		nameLbl.Size = UDim2.new(1, -85, 1, 0)
		nameLbl.Position = UDim2.new(0, 30, 0, 0)
		nameLbl.BackgroundTransparency = 1
		nameLbl.Font = Enum.Font.SourceSansBold
		nameLbl.Text = it.name .. (if it.count > 1 then " x" .. it.count else "")
		nameLbl.TextColor3 = Color3.fromRGB(225, 235, 245)
		nameLbl.TextSize = 13
		nameLbl.TextXAlignment = Enum.TextXAlignment.Left
		nameLbl.Parent = row

		local transferBtn = Instance.new("TextButton")
		transferBtn.Size = UDim2.new(0, 55, 0, 22)
		transferBtn.Position = UDim2.new(1, -60, 0, 6)
		transferBtn.BackgroundColor3 = Color3.fromRGB(45, 105, 65)
		transferBtn.Font = Enum.Font.SourceSansBold
		transferBtn.Text = "Tomar"
		transferBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
		transferBtn.TextSize = 11
		transferBtn.Parent = row

		local tc = Instance.new("UICorner")
		tc.CornerRadius = UDim.new(0, 4)
		tc.Parent = transferBtn

		transferBtn.MouseButton1Click:Connect(function()
			table.insert(playerInventory, it)
			table.remove(currentLootItems, idx)
			renderInventories()
		end)
	end
end

lootAllBtn.MouseButton1Click:Connect(function()
	for _, it in ipairs(currentLootItems) do
		table.insert(playerInventory, it)
	end
	currentLootItems = {}
	renderInventories()
end)

local function updateNearbyContainerLoot(rootPos: Vector3)
	local nearestContainer: Instance? = nil
	local bestDist = 6.5

	for _, desc in ipairs(Workspace:GetDescendants()) do
		if desc:IsA("BasePart") or desc:IsA("Model") then
			local n = string.lower(desc.Name)
			local isCont = n:find("storage") or n:find("counter") or n:find("sink") or n:find("trash") or n:find("table") or n:find("armario") or n:find("escritorio") or n:find("estanteria") or (desc:GetAttribute("IsLootableContainer") == true)
			if isCont then
				local pos = if desc:IsA("BasePart") then desc.Position else (desc:GetPivot().Position)
				local dist = (pos - rootPos).Magnitude
				if dist < bestDist then
					bestDist = dist
					nearestContainer = desc
				end
			end
		end
	end

	if nearestContainer then
		local cName = nearestContainer.Name
		local displayName = "Contenedor"
		if nearestContainer:GetAttribute("IsLootableContainer") == true or cName:find("Zombie") or cName:find("Zombi") then
			displayName = "Cadáver de Zombi"
		elseif cName:find("police") or cName:find("comisaria") then
			displayName = "Armero Policial"
		elseif cName:find("storage") or cName:find("counter") or cName:find("mostrador") then
			displayName = "Mostrador / Estantería"
		elseif cName:find("sink") or cName:find("bathroom") or cName:find("botiquin") then
			displayName = "Botiquín Médico"
		end

		if currentLootContainerName ~= displayName then
			currentLootContainerName = displayName
			currentLootItems = {}
			if displayName == "Cadáver de Zombi" then
				currentLootItems = {
					{ name = "Monedas de Kentucky", weight = 0.1, icon = "🪙", desc = "Monedas antiguas.", category = "Varios", count = 6 },
					{ name = "Reloj Digital", weight = 0.2, icon = "⌚", desc = "Reloj de pulsera.", category = "Herramienta", count = 1 },
					{ name = "Tela Rasgada", weight = 0.1, icon = "🧵", desc = "Tela limpia.", category = "Medicina", count = 2 },
				}
			elseif displayName == "Armero Policial" then
				currentLootItems = {
					{ name = "Caja de Balas 9mm", weight = 0.6, icon = "📦", desc = "30 balas 9mm.", category = "Munición", count = 2 },
					{ name = "Pistola 9mm", weight = 1.2, icon = "🔫", desc = "Arma corta.", category = "Armas", count = 1 },
				}
			elseif displayName == "Botiquín Médico" then
				currentLootItems = {
					{ name = "Vendaje Estéril", weight = 0.15, icon = "🩹", desc = "Vendaje médico.", category = "Medicina", count = 3 },
					{ name = "Alcohol desinfectante", weight = 0.3, icon = "🧪", desc = "Previene infecciones.", category = "Medicina", count = 1 },
					{ name = "Analgésicos", weight = 0.1, icon = "💊", desc = "Alivia dolor.", category = "Medicina", count = 2 },
				}
			else
				currentLootItems = {
					{ name = "Lata de Frijoles", weight = 0.4, icon = "🥫", desc = "Comida imperecedera.", category = "Comida", count = 2 },
					{ name = "Botella de Agua", weight = 0.8, icon = "💧", desc = "Agua potable.", category = "Bebida", count = 1 },
				}
			end
			renderInventories()
		end
	else
		if currentLootContainerName ~= "Suelo" then
			currentLootContainerName = "Suelo"
			currentLootItems = {}
			renderInventories()
		end
	end
end

--------------------------------------------------------------------------------
-- 7. EVENTOS DE ENTRADA Y BUCLE DE SIMULACIÓN (MÓDULOS 5, 6, 7)
--------------------------------------------------------------------------------
heartBtn.MouseButton1Click:Connect(function()
	medicalWindow.Visible = not medicalWindow.Visible
	if medicalWindow.Visible then updateMedicalUI() end
end)

invBtn.MouseButton1Click:Connect(function()
	doubleInventoryWindow.Visible = not doubleInventoryWindow.Visible
	if doubleInventoryWindow.Visible then renderInventories() end
end)

UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end
	if input.KeyCode == Enum.KeyCode.H then
		medicalWindow.Visible = not medicalWindow.Visible
		if medicalWindow.Visible then updateMedicalUI() end
	elseif input.KeyCode == Enum.KeyCode.I then
		doubleInventoryWindow.Visible = not doubleInventoryWindow.Visible
		if doubleInventoryWindow.Visible then renderInventories() end
	end
end)

-- Daño y heridas reales de zombis (MÓDULO 6)
medicalRemote.OnClientEvent:Connect(function(actionType: string, woundType: string)
	if actionType == "Damage" then
		stats.health = math.max(10, stats.health - 16)
		local partsList = { "BrazoIzq", "BrazoDer", "Cuello", "Torso", "PiernaIzq", "PiernaDer" }
		local targetPart = partsList[math.random(1, #partsList)]
		local bp = bodyParts[targetPart]
		if bp then
			bp.status = woundType
			bp.isBleeding = true
			bp.isBandaged = false
			if woundType == "Mordida" then bp.infectionChance = 100
			elseif woundType == "Laceración" then bp.infectionChance = 25
			else bp.infectionChance = 7 end
		end
		updateMedicalUI()
	end
end)

-- Bucle de Reloj, Resistencia, Pánico y Moodles (MÓDULO 7)
task.spawn(function()
	while true do
		task.wait(0.5)

		-- Reloj digital sincronizado con Lighting.ClockTime
		local clock = Lighting.ClockTime
		local hour = math.floor(clock)
		local mins = math.floor((clock - hour) * 60)
		local ampm = if hour >= 12 then "PM" else "AM"
		local displayHour = if hour == 0 then 12 elseif hour > 12 then hour - 12 else hour
		wTime.Text = string.format("%02d:%02d %s", displayHour, mins, ampm)

		-- Recuperación natural de stamina si no corre
		local char = player.Character
		if char then
			local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
			local hum = char:FindFirstChildOfClass("Humanoid")
			if root and hum then
				local isSprinting = hum.WalkSpeed > 18.0
				if isSprinting then
					stats.stamina = math.max(0, stats.stamina - 4.5)
				else
					stats.stamina = math.min(100, stats.stamina + 2.5)
				end

				-- Detección de zombis a menos de 20 studs para Pánico
				local nearbyZombies = 0
				for _, z in ipairs(Workspace:GetDescendants()) do
					if z:IsA("Model") and (z.Name:find("Zombie") or z.Name:find("Zombi")) then
						local zRoot = z:FindFirstChild("HumanoidRootPart") :: BasePart?
						local zHum = z:FindFirstChildOfClass("Humanoid")
						if zRoot and zHum and zHum.Health > 0 then
							if (zRoot.Position - root.Position).Magnitude <= 20.0 then
								nearbyZombies += 1
							end
						end
					end
				end

				if nearbyZombies >= 2 then
					stats.panic = math.min(100, stats.panic + 12)
					if not heartbeatSound.IsPlaying then heartbeatSound:Play() end
				else
					stats.panic = math.max(0, stats.panic - 8)
					if heartbeatSound.IsPlaying then heartbeatSound:Stop() end
				end

				-- Detección de botín
				if doubleInventoryWindow.Visible then
					updateNearbyContainerLoot(root.Position)
				end

				-- Moodles y Sangrado
				local anyBleeding = false
				for _, bp in pairs(bodyParts) do
					if bp.isBleeding then anyBleeding = true break end
				end

				moodleButtons.Bleeding.btn.Visible = anyBleeding
				moodleButtons.Panic.btn.Visible = (stats.panic > 20)
				moodleButtons.Exhaustion.btn.Visible = (stats.stamina < 30)
				moodleButtons.Hunger.btn.Visible = (stats.hunger > 40)
				moodleButtons.Thirst.btn.Visible = (stats.thirst > 35)
				moodleButtons.HeavyLoad.btn.Visible = (calcTotalWeight(playerInventory) > 12.0)

				-- Hemorragia drena vida
				if anyBleeding then
					stats.health = math.max(5, stats.health - 1.0)
					hum.Health = stats.health
				end
			end
		end
	end
end)

renderInventories()
updateMedicalUI()
