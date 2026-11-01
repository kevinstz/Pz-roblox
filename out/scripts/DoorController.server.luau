--!strict
-- DoorController.server.luau
-- MÓDULO 2 & MÓDULO 1: Sistema Anti-Catapultaje, Física de Puertas (PhysicsService) y Rampas de Escaleras
local TweenService = game:GetService("TweenService")
local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PhysicsService = game:GetService("PhysicsService")

local DOOR_TWEEN_INFO = TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)

-- 1. CONFIGURACIÓN DE GRUPOS DE COLISIÓN (PhysicsService)
pcall(function() PhysicsService:RegisterCollisionGroup("Doors") end)
pcall(function() PhysicsService:RegisterCollisionGroup("Characters") end)
pcall(function() PhysicsService:CollisionGroupSetCollidable("Doors", "Characters", false) end)

-- Folder de Remotes
local remotes = ReplicatedStorage:FindFirstChild("PZ_Remotes")
if not remotes then
	local f = Instance.new("Folder")
	f.Name = "PZ_Remotes"
	f.Parent = ReplicatedStorage
	remotes = f
end

local doorInteractRemote = remotes:FindFirstChild("PZ_DoorInteract") or Instance.new("RemoteEvent")
doorInteractRemote.Name = "PZ_DoorInteract"
doorInteractRemote.Parent = remotes

-- 2. BLOQUEO DE TREPADO Y RESPAWN LIMPIO AL NIVEL DEL SUELO (MÓDULO 2.1)
local SPAWN_STREET_POS = Vector3.new(0, 3.5, 0)

local function configureSurvivorHumanoid(char: Model)
	local hrp = char:WaitForChild("HumanoidRootPart", 5) :: BasePart?
	local hum = char:WaitForChild("Humanoid", 5) :: Humanoid?
	if not hrp or not hum then return end

	-- Teletransporte seguro a la calle Rosewood en Y = 3.5 (nunca en tejados)
	task.wait(0.1)
	hrp.CFrame = CFrame.new(SPAWN_STREET_POS)
	hrp.AssemblyLinearVelocity = Vector3.zero
	hrp.AssemblyAngularVelocity = Vector3.zero

	-- Físicas estrictas de Project Zomboid Build 42
	hum:SetStateEnabled(Enum.HumanoidStateType.Climbing, false)
	hum.MaxSlopeAngle = 40.0
	hum.AutoJumpEnabled = false
	hum.UseJumpPower = true
	hum.JumpPower = 0.0 -- En PZ no se salta verticalmente; Espacio es Shove

	-- Asignar grupo de colisión Characters
	for _, part in ipairs(char:GetDescendants()) do
		if part:IsA("BasePart") then
			pcall(function() part.CollisionGroup = "Characters" end)
		end
	end
end

Players.PlayerAdded:Connect(function(pl)
	pl.CharacterAdded:Connect(configureSurvivorHumanoid)
	if pl.Character then configureSurvivorHumanoid(pl.Character) end
end)

for _, pl in ipairs(Players:GetPlayers()) do
	if pl.Character then configureSurvivorHumanoid(pl.Character) end
end

-- 3. FÍSICA DE PUERTAS CON BISAGRAS LATERALES REALES (MÓDULO 2.2)
local doorRegistry: { [BasePart]: { toggle: () -> () } } = {}

local function setupDoor(part: BasePart)
	local nameLower = string.lower(part.Name)
	local isDoor = nameLower:find("puerta") or nameLower:find("fixtures_doors_")
	if not isDoor or nameLower:find("frame") or nameLower:find("frames") then return end
	if doorRegistry[part] then return end

	pcall(function() part.CollisionGroup = "Doors" end)

	local closedCFrame = part.CFrame
	local baseSize = part.Size

	local sx, sy, sz = baseSize.X, baseSize.Y, baseSize.Z
	local width = math.max(sx, sz)
	if sy > sx and sy > sz then width = math.max(sx, sz) end

	local rightVec = closedCFrame.RightVector
	local lookVec = closedCFrame.LookVector
	local widthDir = if math.abs(rightVec.Y) < 0.5 then rightVec else lookVec
	local flatWidthDir = Vector3.new(widthDir.X, 0, widthDir.Z).Unit

	-- Bisagra lateral en el borde del marco (no en el centro)
	local hingePos = closedCFrame.Position - (flatWidthDir * (width * 0.48))
	local offsetFromHinge = hingePos - closedCFrame.Position

	local rot = CFrame.Angles(0, math.rad(90), 0)
	local openCFrame = CFrame.new(hingePos) * rot * CFrame.new(-offsetFromHinge) * (closedCFrame - closedCFrame.Position)

	local isOpen = false
	local isBusy = false

	local openSound = Instance.new("Sound")
	openSound.Name = "DoorOpenSound"
	openSound.SoundId = "rbxasset://sounds/door_open.mp3"
	openSound.Volume = 0.65
	openSound.Parent = part

	local closeSound = Instance.new("Sound")
	closeSound.Name = "DoorCloseSound"
	closeSound.SoundId = "rbxasset://sounds/door_close.mp3"
	closeSound.Volume = 0.65
	closeSound.Parent = part

	local prompt = part:FindFirstChildOfClass("ProximityPrompt") or Instance.new("ProximityPrompt")
	prompt.ActionText = "Abrir / Cerrar [E]"
	prompt.ObjectText = "Puerta"
	prompt.KeyboardKeyCode = Enum.KeyCode.E
	prompt.MaxActivationDistance = 6.5
	prompt.RequiresLineOfSight = false
	prompt.HoldDuration = 0
	prompt.UIOffset = Vector2.new(0, 15)
	prompt.Parent = part

	local function toggleDoor()
		if isBusy then return end
		isBusy = true
		isOpen = not isOpen

		-- CERO CATAPULTAJE: CanCollide = false ANTES de iniciar movimiento
		part.CanCollide = false

		if isOpen then
			pcall(function() openSound:Play() end)
			local tween = TweenService:Create(part, DOOR_TWEEN_INFO, { CFrame = openCFrame })
			tween:Play()
			tween.Completed:Connect(function()
				part.CanCollide = false
				isBusy = false
			end)
		else
			pcall(function() closeSound:Play() end)
			local tween = TweenService:Create(part, DOOR_TWEEN_INFO, { CFrame = closedCFrame })
			tween:Play()
			tween.Completed:Connect(function()
				task.wait(0.1)
				if not isOpen then
					part.CanCollide = true
				end
				isBusy = false
			end)
		end
	end

	prompt.Triggered:Connect(toggleDoor)
	doorRegistry[part] = { toggle = toggleDoor }
end

doorInteractRemote.OnServerEvent:Connect(function(player, doorPart)
	if not doorPart or not doorPart:IsA("BasePart") then return end
	local pChar = player.Character
	if not pChar then return end
	local pRoot = pChar:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not pRoot then return end

	if (pRoot.Position - doorPart.Position).Magnitude <= 7.5 then
		local reg = doorRegistry[doorPart]
		if reg then reg.toggle() end
	end
end)

for _, desc in ipairs(Workspace:GetDescendants()) do
	if desc:IsA("BasePart") then setupDoor(desc) end
end

Workspace.DescendantAdded:Connect(function(desc)
	if desc:IsA("BasePart") then
		task.wait(0.2)
		setupDoor(desc)
	end
end)

-- 4. RAMPAS DE COLISIÓN EN ESCALERAS (MÓDULO 1.2)
-- Crea rampas invisibles lisas inclinadas a 36° para que el Humanoid suba sin atorarse
local function generateStairRamps()
	local map = Workspace:FindFirstChild("PZ_Rosewood_B42")
	if not map then return end
	local edifFolder = map:FindFirstChild("Edificios")
	if not edifFolder then return end

	local rampFolder = map:FindFirstChild("PZ_StairRamps")
	if not rampFolder then
		rampFolder = Instance.new("Folder")
		rampFolder.Name = "PZ_StairRamps"
		rampFolder.Parent = map
	end

	for _, bld in ipairs(edifFolder:GetChildren()) do
		if bld:IsA("Model") then
			local stairsList: { BasePart } = {}
			for _, desc in ipairs(bld:GetDescendants()) do
				if desc:IsA("BasePart") and desc.Name:find("fixtures_stairs_") then
					table.insert(stairsList, desc)
				end
			end

			if #stairsList >= 3 then
				local minX, maxX = Infinity, -Infinity
				local minY, maxY = Infinity, -Infinity
				local minZ, maxZ = Infinity, -Infinity

				for _, p in ipairs(stairsList) do
					local pos = p.Position
					if pos.X < minX then minX = pos.X end
					if pos.X > maxX then maxX = pos.X end
					if pos.Y < minY then minY = pos.Y end
					if pos.Y > maxY then maxY = pos.Y end
					if pos.Z < minZ then minZ = pos.Z end
					if pos.Z > maxZ then maxZ = pos.Z end
				end

				local dx = maxX - minX
				local dy = maxY - minY
				local dz = maxZ - minZ

				-- Crear rampa de colisión
				local ramp = Instance.new("Part")
				ramp.Name = "StairCollisionRamp_" .. bld.Name
				ramp.Anchored = true
				ramp.CanCollide = true
				ramp.Transparency = 1 -- Invisible
				ramp.Material = Enum.Material.SmoothPlastic
				ramp.Friction = 0.6

				local midX = (minX + maxX) * 0.5
				local midY = (minY + maxY) * 0.5
				local midZ = (minZ + maxZ) * 0.5

				if dx > dz then
					-- Rampa orientada en eje X
					local len = math.sqrt(dx * dx + dy * dy)
					ramp.Size = Vector3.new(len, 0.4, math.max(dz + 2.0, 3.5))
					local angle = math.atan2(dy, dx)
					ramp.CFrame = CFrame.new(midX, midY, midZ) * CFrame.Angles(0, 0, angle)
				else
					-- Rampa orientada en eje Z
					local len = math.sqrt(dz * dz + dy * dy)
					ramp.Size = Vector3.new(math.max(dx + 2.0, 3.5), 0.4, len)
					local angle = math.atan2(dy, dz)
					ramp.CFrame = CFrame.new(midX, midY, midZ) * CFrame.Angles(-angle, 0, 0)
				end

				ramp.Parent = rampFolder
			end
		end
	end
end

task.spawn(function()
	task.wait(1.0)
	generateStairRamps()
end)
