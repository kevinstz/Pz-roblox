--!strict
-- SurvivorCombatController.client.luau
-- MÓDULO 4: Combate Isométrico Real, Apuntado con Clic Derecho, Animaciones Procedurales y Empujón
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local camera = Workspace.CurrentCamera

-- Variables de Estado
local isAiming = false
local isSprinting = false
local isAttacking = false
local isShoving = false
local lastAttackTime = 0
local lastShoveTime = 0
local currentSlot = 1 -- 1: Bate, 2: Pistola 9mm, 3: Vendaje
local pistolAmmo = 15
local maxPistolAmmo = 15
local isReloading = false

local ATTACK_COOLDOWN_BAT = 0.50
local ATTACK_COOLDOWN_GUN = 0.35
local SHOVE_COOLDOWN = 0.70

-- RemoteEvents
local remotes = ReplicatedStorage:WaitForChild("PZ_Remotes", 10) :: Folder
local attackRemote = remotes:WaitForChild("PZ_Attack", 10) :: RemoteEvent
local shoveRemote = remotes:WaitForChild("PZ_Shove", 10) :: RemoteEvent
local gunshotRemote = remotes:WaitForChild("PZ_GunshotAlert", 10) :: RemoteEvent

-- Sonidos
local swingSound = Instance.new("Sound")
swingSound.Name = "SwingSound"
swingSound.SoundId = "rbxasset://sounds/sword_swing.mp3"
swingSound.Volume = 0.8
swingSound.Parent = camera

local hitSound = Instance.new("Sound")
hitSound.Name = "HitSound"
hitSound.SoundId = "rbxasset://sounds/impact_hit.mp3"
hitSound.Volume = 0.95
hitSound.Parent = camera

local gunSound = Instance.new("Sound")
gunSound.Name = "GunSound"
gunSound.SoundId = "rbxasset://sounds/electronicpingshort.wav"
gunSound.Volume = 1.0
gunSound.Parent = camera

local shoveSound = Instance.new("Sound")
shoveSound.Name = "ShoveSound"
shoveSound.SoundId = "rbxasset://sounds/action_footsteps_plastic.mp3"
shoveSound.Volume = 0.75
shoveSound.Parent = camera

-- Marcador de suelo para apuntado isométrico
local aimCursorPart = Instance.new("Part")
aimCursorPart.Name = "PZ_AimCursor"
aimCursorPart.Shape = Enum.PartType.Cylinder
aimCursorPart.Size = Vector3.new(0.04, 1.6, 1.6)
aimCursorPart.Material = Enum.Material.Neon
aimCursorPart.Color = Color3.fromRGB(220, 60, 50)
aimCursorPart.Transparency = 1
aimCursorPart.CanCollide = false
aimCursorPart.Anchored = true
aimCursorPart.CFrame = CFrame.Angles(0, 0, math.rad(90))
aimCursorPart.Parent = Workspace

-- Modelos de Armas en Mano Derecha
local equippedWeaponModel: Model? = nil

local function getRightHand(char: Model): BasePart?
	return (char:FindFirstChild("RightHand") or char:FindFirstChild("Right Arm")) :: BasePart?
end

local function clearEquippedWeapon()
	if equippedWeaponModel then
		equippedWeaponModel:Destroy()
		equippedWeaponModel = nil
	end
end

local function equipWeapon(slot: number)
	currentSlot = slot
	clearEquippedWeapon()

	local char = player.Character
	if not char then return end
	local hand = getRightHand(char)
	if not hand then return end

	local wModel = Instance.new("Model")
	wModel.Name = "EquippedWeapon"

	if slot == 1 then
		-- Bate de béisbol con clavos
		local bat = Instance.new("Part")
		bat.Name = "BaseballBat"
		bat.Shape = Enum.PartType.Cylinder
		bat.Size = Vector3.new(3.2, 0.35, 0.35)
		bat.Material = Enum.Material.Wood
		bat.Color = Color3.fromRGB(155, 105, 55)
		bat.CanCollide = false
		bat.Massless = true
		bat.Parent = wModel

		local weld = Instance.new("WeldConstraint")
		weld.Part0 = hand
		weld.Part1 = bat
		bat.CFrame = hand.CFrame * CFrame.new(0, -0.6, 0.6) * CFrame.Angles(math.rad(45), 0, 0)
		weld.Parent = bat
	elseif slot == 2 then
		-- Pistola 9mm
		local pistol = Instance.new("Part")
		pistol.Name = "Pistol9mm"
		pistol.Shape = Enum.PartType.Block
		pistol.Size = Vector3.new(0.28, 0.6, 0.95)
		pistol.Material = Enum.Material.Metal
		pistol.Color = Color3.fromRGB(35, 35, 40)
		pistol.CanCollide = false
		pistol.Massless = true
		pistol.Parent = wModel

		local muzzleLight = Instance.new("PointLight")
		muzzleLight.Name = "MuzzleLight"
		muzzleLight.Brightness = 4
		muzzleLight.Range = 16
		muzzleLight.Color = Color3.fromRGB(255, 200, 100)
		muzzleLight.Enabled = false
		muzzleLight.Parent = pistol

		local weld = Instance.new("WeldConstraint")
		weld.Part0 = hand
		weld.Part1 = pistol
		pistol.CFrame = hand.CFrame * CFrame.new(0, -0.5, 0.4) * CFrame.Angles(0, 0, 0)
		weld.Parent = pistol
	end

	wModel.Parent = char
	equippedWeaponModel = wModel

	local hudEvent = ReplicatedStorage:FindFirstChild("PZ_HUD_UpdateSlot") :: BindableEvent?
	if hudEvent then hudEvent:Fire(slot, pistolAmmo) end
end

-- Detectar zombis en un arco frontal
local function getZombiesInFront(maxRange: number, maxAngleDeg: number): { Model }
	local char = player.Character
	if not char then return {} end
	local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return {} end

	local pPos = root.Position
	local pLook = root.CFrame.LookVector
	local results: { Model } = {}

	for _, obj in ipairs(Workspace:GetDescendants()) do
		if obj:IsA("Model") and (obj.Name:find("Zombie") or obj.Name:find("Zombi")) then
			local zRoot = obj:FindFirstChild("HumanoidRootPart") :: BasePart?
			local zHum = obj:FindFirstChildOfClass("Humanoid")
			if zRoot and zHum and zHum.Health > 0 then
				local toZombie = zRoot.Position - pPos
				local dist = toZombie.Magnitude
				if dist <= maxRange then
					local dirToZ = toZombie.Unit
					local dot = pLook:Dot(dirToZ)
					local angle = math.deg(math.acos(math.clamp(dot, -1, 1)))
					if angle <= maxAngleDeg then
						table.insert(results, obj)
					end
				end
			end
		end
	end
	return results
end

-- Generar partículas de sangre rojas en impacto
local function spawnBloodEffect(position: Vector3)
	local bloodEmitterPart = Instance.new("Part")
	bloodEmitterPart.Size = Vector3.new(0.2, 0.2, 0.2)
	bloodEmitterPart.Position = position
	bloodEmitterPart.Transparency = 1
	bloodEmitterPart.Anchored = true
	bloodEmitterPart.CanCollide = false
	bloodEmitterPart.Parent = Workspace

	local emitter = Instance.new("ParticleEmitter")
	emitter.Color = ColorSequence.new(Color3.fromRGB(180, 20, 20), Color3.fromRGB(110, 10, 10))
	emitter.Size = NumberSequence.new(0.3, 0.1)
	emitter.Speed = NumberRange.new(4, 8)
	emitter.SpreadAngle = Vector2.new(45, 45)
	emitter.Lifetime = NumberRange.new(0.3, 0.6)
	emitter.Rate = 0
	emitter.Parent = bloodEmitterPart

	emitter:Emit(15)
	task.delay(1.0, function() bloodEmitterPart:Destroy() end)
end

-- Acción de Ataque con Clic Izquierdo (LMB)
local function doAttack(mouseHitPos: Vector3)
	local now = os.clock()
	local cooldown = if currentSlot == 2 then ATTACK_COOLDOWN_GUN else ATTACK_COOLDOWN_BAT
	if now - lastAttackTime < cooldown or isShoving or isReloading then return end
	lastAttackTime = now
	isAttacking = true

	local char = player.Character
	if not char then return end
	local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end

	-- Drenar stamina por ataque
	local staminaEvent = ReplicatedStorage:FindFirstChild("PZ_HUD_DrainStamina") :: BindableEvent?
	if staminaEvent then staminaEvent:Fire(if currentSlot == 1 then 8.0 else 3.0) end

	if currentSlot == 1 then
		-- ATAQUE CON BATE (Swing animado)
		pcall(function() swingSound:Play() end)

		-- Animación procedural rápida del hombro derecho
		local torso = char:FindFirstChild("Torso") or char:FindFirstChild("UpperTorso")
		local shoulder = if torso then torso:FindFirstChild("Right Shoulder") :: Motor6D? else nil
		if shoulder then
			local origC0 = shoulder.C0
			shoulder.C0 = origC0 * CFrame.Angles(math.rad(60), math.rad(-70), math.rad(45))
			task.delay(0.25, function() shoulder.C0 = origC0 end)
		end

		local targets = getZombiesInFront(6.5, 75.0)
		if #targets > 0 then
			pcall(function() hitSound:Play() end)
			for _, z in ipairs(targets) do
				local zRoot = z:FindFirstChild("HumanoidRootPart") :: BasePart?
				if zRoot then spawnBloodEffect(zRoot.Position + Vector3.new(0, 1.0, 0)) end
				attackRemote:FireServer(z, 35.0, "Bat")
			end
		end
	elseif currentSlot == 2 then
		-- DISPARO CON PISTOLA 9MM
		if pistolAmmo > 0 then
			pistolAmmo -= 1
			pcall(function() gunSound:Play() end)

			if equippedWeaponModel then
				local pPart = equippedWeaponModel:FindFirstChild("Pistol9mm")
				if pPart then
					local mLight = pPart:FindFirstChild("MuzzleLight") :: PointLight?
					if mLight then
						mLight.Enabled = true
						task.delay(0.08, function() mLight.Enabled = false end)
					end
				end
			end

			-- Alerta a zombis en 90 studs (MÓDULO 4.2)
			gunshotRemote:FireServer(root.Position, 90.0)

			local origin = root.Position + Vector3.new(0, 1.5, 0)
			local dir = (mouseHitPos - origin).Unit * 130.0
			local rayParams = RaycastParams.new()
			rayParams.FilterType = Enum.RaycastFilterType.Exclude
			rayParams.FilterDescendantsInstances = { char, aimCursorPart }

			local hit = Workspace:Raycast(origin, dir, rayParams)
			if hit and hit.Instance then
				local hitModel = hit.Instance:FindFirstAncestorOfClass("Model")
				if hitModel and (hitModel.Name:find("Zombie") or hitModel.Name:find("Zombi")) then
					local isHead = (hit.Instance.Name == "Head")
					local dmg = if isHead then 100.0 else 70.0
					local zRoot = hitModel:FindFirstChild("HumanoidRootPart") :: BasePart?
					if zRoot then spawnBloodEffect(hit.Position) end
					attackRemote:FireServer(hitModel, dmg, if isHead then "Headshot" else "Pistol")
				end
			end

			local hudEvent = ReplicatedStorage:FindFirstChild("PZ_HUD_UpdateSlot") :: BindableEvent?
			if hudEvent then hudEvent:Fire(currentSlot, pistolAmmo) end
		else
			pcall(function() swingSound:Play() end)
		end
	elseif currentSlot == 3 then
		-- APLICAR VENDAJE
		local medRemote = remotes:FindFirstChild("PZ_Medical") :: RemoteEvent?
		if medRemote then medRemote:FireServer("BandageSelf") end
	end

	task.delay(0.2, function() isAttacking = false end)
end

-- Recarga de Pistola con Tecla R
local function reloadPistol()
	if currentSlot ~= 2 or isReloading or pistolAmmo >= maxPistolAmmo then return end
	isReloading = true
	task.delay(1.5, function()
		pistolAmmo = maxPistolAmmo
		isReloading = false
		local hudEvent = ReplicatedStorage:FindFirstChild("PZ_HUD_UpdateSlot") :: BindableEvent?
		if hudEvent then hudEvent:Fire(currentSlot, pistolAmmo) end
	end)
end

-- Acción de Empujón (Space)
local function doShove()
	local now = os.clock()
	if now - lastShoveTime < SHOVE_COOLDOWN or isAttacking then return end
	lastShoveTime = now
	isShoving = true

	local staminaEvent = ReplicatedStorage:FindFirstChild("PZ_HUD_DrainStamina") :: BindableEvent?
	if staminaEvent then staminaEvent:Fire(6.0) end

	pcall(function() shoveSound:Play() end)

	-- Animación procedural de empujón con ambos brazos
	local char = player.Character
	if char then
		local torso = char:FindFirstChild("Torso") or char:FindFirstChild("UpperTorso")
		if torso then
			local rShoulder = torso:FindFirstChild("Right Shoulder") :: Motor6D?
			local lShoulder = torso:FindFirstChild("Left Shoulder") :: Motor6D?
			if rShoulder and lShoulder then
				local origR = rShoulder.C0
				local origL = lShoulder.C0
				rShoulder.C0 = origR * CFrame.Angles(math.rad(90), 0, math.rad(-15))
				lShoulder.C0 = origL * CFrame.Angles(math.rad(90), 0, math.rad(15))
				task.delay(0.3, function()
					rShoulder.C0 = origR
					lShoulder.C0 = origL
				end)
			end
		end
	end

	local targets = getZombiesInFront(5.5, 85.0)
	for _, z in ipairs(targets) do
		shoveRemote:FireServer(z)
	end

	task.delay(0.35, function() isShoving = false end)
end

-- Controles de Entrada
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = true
	elseif input.UserInputType == Enum.UserInputType.MouseButton1 then
		if isAiming then
			local mouseLoc = UserInputService:GetMouseLocation()
			local ray = camera:ViewportPointToRay(mouseLoc.X, mouseLoc.Y)
			local t = -ray.Origin.Y / ray.Direction.Y
			local groundPos = ray.Origin + ray.Direction * math.max(t, 10)
			doAttack(groundPos)
		end
	elseif input.KeyCode == Enum.KeyCode.Space then
		doShove()
	elseif input.KeyCode == Enum.KeyCode.R then
		reloadPistol()
	elseif input.KeyCode == Enum.KeyCode.One then
		equipWeapon(1)
	elseif input.KeyCode == Enum.KeyCode.Two then
		equipWeapon(2)
	elseif input.KeyCode == Enum.KeyCode.Three then
		equipWeapon(3)
	elseif input.KeyCode == Enum.KeyCode.E then
		-- Vault o interactuar con puerta
		local char = player.Character
		if char then
			local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local nearestDoor: BasePart? = nil
				local bestDist = 6.8
				for _, desc in ipairs(Workspace:GetDescendants()) do
					if desc:IsA("BasePart") and (desc.Name:find("Puerta") or desc.Name:find("fixtures_doors_")) then
						local dist = (desc.Position - root.Position).Magnitude
						if dist < bestDist then
							bestDist = dist
							nearestDoor = desc
						end
					end
				end
				if nearestDoor then
					local dRemote = remotes:FindFirstChild("PZ_DoorInteract") :: RemoteEvent?
					if dRemote then dRemote:FireServer(nearestDoor) end
				end
			end
		end
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

-- Bucle de Control y Apuntado Isométrico
RunService.RenderStepped:Connect(function(dt: number)
	local char = player.Character
	if not char then return end
	local hum = char:FindFirstChildOfClass("Humanoid")
	local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not hum or not root or hum.Health <= 0 then
		aimCursorPart.Transparency = 1
		return
	end

	local torso = char:FindFirstChild("Torso") or char:FindFirstChild("UpperTorso")
	local rShoulder = if torso then torso:FindFirstChild("Right Shoulder") :: Motor6D? else nil

	if isAiming then
		hum.WalkSpeed = 8.0 -- Velocidad táctica PZ
		hum.AutoRotate = false

		-- Elevación procedural del brazo derecho al apuntar
		if rShoulder and not isAttacking and not isShoving then
			rShoulder.Transform = CFrame.Angles(math.rad(85), 0, math.rad(-10))
		end

		local mouseLoc = UserInputService:GetMouseLocation()
		local ray = camera:ViewportPointToRay(mouseLoc.X, mouseLoc.Y)
		local groundY = root.Position.Y
		local t = (groundY - ray.Origin.Y) / ray.Direction.Y
		if t > 0 then
			local hitPos = ray.Origin + ray.Direction * t
			aimCursorPart.Position = Vector3.new(hitPos.X, groundY + 0.05, hitPos.Z)
			aimCursorPart.Transparency = 0.35

			local toCursor = Vector3.new(hitPos.X - root.Position.X, 0, hitPos.Z - root.Position.Z)
			if toCursor.Magnitude > 0.4 then
				local targetCFrame = CFrame.lookAt(root.Position, root.Position + toCursor.Unit)
				root.CFrame = root.CFrame:Lerp(targetCFrame, math.clamp(dt * 18.0, 0, 1))
			end
		end
	else
		aimCursorPart.Transparency = 1
		hum.AutoRotate = true
		hum.WalkSpeed = if isSprinting then 22.0 else 14.0
	end
end)

player.CharacterAdded:Connect(function()
	task.wait(0.5)
	equipWeapon(currentSlot)
end)

equipWeapon(1)
