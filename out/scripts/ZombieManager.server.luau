--!strict
-- ZombieManager.server.luau
-- MÓDULO 8: IA de 35 Zombis Shamblers con Animación R6 Procedural, Sonido y Saqueo de Cadáveres
local PathfindingService = game:GetService("PathfindingService")
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local remotes = ReplicatedStorage:FindFirstChild("PZ_Remotes")
if not remotes then
	local f = Instance.new("Folder")
	f.Name = "PZ_Remotes"
	f.Parent = ReplicatedStorage
	remotes = f
end

local attackRemote = remotes:FindFirstChild("PZ_Attack") or Instance.new("RemoteEvent")
attackRemote.Name = "PZ_Attack"
attackRemote.Parent = remotes

local shoveRemote = remotes:FindFirstChild("PZ_Shove") or Instance.new("RemoteEvent")
shoveRemote.Name = "PZ_Shove"
shoveRemote.Parent = remotes

local medicalRemote = remotes:FindFirstChild("PZ_Medical") or Instance.new("RemoteEvent")
medicalRemote.Name = "PZ_Medical"
medicalRemote.Parent = remotes

local gunshotRemote = remotes:FindFirstChild("PZ_GunshotAlert") or Instance.new("RemoteEvent")
gunshotRemote.Name = "PZ_GunshotAlert"
gunshotRemote.Parent = remotes

--------------------------------------------------------------------------------
-- MANEJO DE ATAQUE Y MUERTE (CADÁVER SAQUEABLE)
--------------------------------------------------------------------------------
attackRemote.OnServerEvent:Connect(function(player, targetZombie, damage, attackType)
	if not targetZombie or not targetZombie:IsA("Model") then return end
	local hum = targetZombie:FindFirstChildOfClass("Humanoid")
	local root = targetZombie:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not hum or not root or hum.Health <= 0 then return end

	local pChar = player.Character
	if not pChar then return end
	local pRoot = pChar:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not pRoot then return end

	local finalDmg = damage or 35.0
	hum:TakeDamage(finalDmg)

	-- Retroceso físico
	local knockbackDir = (root.Position - pRoot.Position).Unit
	root.AssemblyLinearVelocity = knockbackDir * 22.0 + Vector3.new(0, 3, 0)

	-- Muerte del zombi -> Convertir en cadáver tendido en el suelo saqueable (MÓDULO 8.1)
	if hum.Health <= 0 then
		targetZombie:SetAttribute("IsDead", true)
		targetZombie:SetAttribute("IsLootableContainer", true)
		hum.PlatformStand = true

		pcall(function()
			root.CFrame = root.CFrame * CFrame.Angles(math.rad(90), 0, 0)
			root.Anchored = true
			for _, part in ipairs(targetZombie:GetDescendants()) do
				if part:IsA("BasePart") then part.CanCollide = false end
			end
		end)

		task.delay(75, function()
			targetZombie:Destroy()
		end)
	end
end)

-- Manejo de Empujón (Shove con 45% probabilidad de derribo al suelo)
shoveRemote.OnServerEvent:Connect(function(player, targetZombie)
	if not targetZombie or not targetZombie:IsA("Model") then return end
	local hum = targetZombie:FindFirstChildOfClass("Humanoid")
	local root = targetZombie:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not hum or not root or hum.Health <= 0 then return end

	local pChar = player.Character
	if not pChar then return end
	local pRoot = pChar:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not pRoot then return end

	if (pRoot.Position - root.Position).Magnitude > 8.0 then return end

	local isKnockedDown = (math.random(1, 100) <= 45)
	if isKnockedDown then
		targetZombie:SetAttribute("StunnedUntil", os.clock() + 2.5)
		hum.PlatformStand = true
		pcall(function()
			root.CFrame = root.CFrame * CFrame.Angles(math.rad(90), 0, 0)
		end)
		task.delay(2.5, function()
			if hum and hum.Health > 0 then
				hum.PlatformStand = false
				root.CFrame = CFrame.new(root.Position)
			end
		end)
	else
		targetZombie:SetAttribute("StunnedUntil", os.clock() + 1.2)
	end

	local pushDir = (root.Position - pRoot.Position).Unit
	root.AssemblyLinearVelocity = pushDir * 28.0 + Vector3.new(0, 4, 0)
end)

-- Alerta de Disparo de Arma de Fuego (Radio de 90 studs)
local alertedPositions: { [Model]: Vector3 } = {}

gunshotRemote.OnServerEvent:Connect(function(player, gunshotPos, radius)
	local rad = radius or 90.0
	for _, desc in ipairs(Workspace:GetDescendants()) do
		if desc:IsA("Model") and (desc.Name:find("Zombie") or desc.Name:find("Zombi")) then
			local root = desc:FindFirstChild("HumanoidRootPart") :: BasePart?
			local hum = desc:FindFirstChildOfClass("Humanoid")
			if root and hum and hum.Health > 0 then
				if (root.Position - gunshotPos).Magnitude <= rad then
					alertedPositions[desc] = gunshotPos
				end
			end
		end
	end
end)

--------------------------------------------------------------------------------
-- IA CON ANIMACIÓN R6 PROCEDURAL, VISIÓN Y PATHFINDING
--------------------------------------------------------------------------------
local function setupZombieAI(zombie: Model)
	if zombie:GetAttribute("HasAI") then return end
	zombie:SetAttribute("HasAI", true)

	local hum = zombie:WaitForChild("Humanoid", 5) :: Humanoid?
	local root = zombie:WaitForChild("HumanoidRootPart", 5) :: BasePart?
	local torso = zombie:FindFirstChild("Torso") :: BasePart?
	local head = zombie:FindFirstChild("Head") :: BasePart?
	if not hum or not root or not torso then return end

	local spawnPos = root.Position
	local biteCooldown = 0
	local isBiting = false

	-- Motor6Ds para animación procedural
	local rShoulder = torso:FindFirstChild("Right Shoulder") :: Motor6D?
	local lShoulder = torso:FindFirstChild("Left Shoulder") :: Motor6D?
	local rHip = torso:FindFirstChild("Right Hip") :: Motor6D?
	local lHip = torso:FindFirstChild("Left Hip") :: Motor6D?
	local neck = torso:FindFirstChild("Neck") :: Motor6D?

	local rShoulderOrig = if rShoulder then rShoulder.C0 else CFrame.new()
	local lShoulderOrig = if lShoulder then lShoulder.C0 else CFrame.new()
	local rHipOrig = if rHip then rHip.C0 else CFrame.new()
	local lHipOrig = if lHip then lHip.C0 else CFrame.new()
	local neckOrig = if neck then neck.C0 else CFrame.new()

	-- Gruñido espacial 3D
	local groanSound = Instance.new("Sound")
	groanSound.Name = "GroanSound"
	groanSound.SoundId = "rbxasset://sounds/action_eating_grass.mp3"
	groanSound.Volume = 0.85
	groanSound.RollOffMode = Enum.RollOffMode.InverseTapered
	groanSound.RollOffMinDistance = 5
	groanSound.RollOffMaxDistance = 60
	groanSound.Parent = head or root

	-- Animación Procedural R6 en Heartbeat
	local animTime = math.random() * 10
	local hbConn: RBXScriptConnection? = nil
	hbConn = RunService.Heartbeat:Connect(function(dt: number)
		if not hum or hum.Health <= 0 or not zombie.Parent or hum.PlatformStand then
			if hbConn then hbConn:Disconnect() end
			return
		end

		animTime += dt * 3.5
		local isMoving = root.AssemblyLinearVelocity.Magnitude > 0.5

		-- Brazos extendidos hacia adelante con leve balanceo (Pose Shambler PZ)
		if rShoulder and lShoulder then
			if isBiting then
				-- Zarpazo/mordida
				rShoulder.C0 = rShoulderOrig * CFrame.Angles(math.rad(110), 0, math.rad(-20))
				lShoulder.C0 = lShoulderOrig * CFrame.Angles(math.rad(110), 0, math.rad(20))
			else
				local armSway = math.sin(animTime * 0.8) * 0.1
				rShoulder.C0 = rShoulderOrig * CFrame.Angles(math.rad(80) + armSway, 0, math.rad(-8))
				lShoulder.C0 = lShoulderOrig * CFrame.Angles(math.rad(80) - armSway, 0, math.rad(8))
			end
		end

		-- Piernas arrastrándose al caminar
		if rHip and lHip then
			if isMoving then
				local legSwing = math.sin(animTime) * 0.55
				rHip.C0 = rHipOrig * CFrame.Angles(-legSwing, 0, 0)
				lHip.C0 = lHipOrig * CFrame.Angles(legSwing, 0, 0)
			else
				rHip.C0 = rHipOrig
				lHip.C0 = lHipOrig
			end
		end

		-- Cuello inclinado
		if neck then
			neck.C0 = neckOrig * CFrame.Angles(math.rad(-10), math.sin(animTime * 0.5) * 0.15, 0)
		end
	end)

	local function hasLineOfSight(targetPos: Vector3): boolean
		local eyePos = if head then head.Position else root.Position + Vector3.new(0, 1.5, 0)
		local dir = targetPos - eyePos
		local rayParams = RaycastParams.new()
		rayParams.FilterType = Enum.RaycastFilterType.Exclude
		rayParams.FilterDescendantsInstances = { zombie }
		local hit = Workspace:Raycast(eyePos, dir, rayParams)
		if hit and hit.Instance then
			local hitModel = hit.Instance:FindFirstAncestorOfClass("Model")
			if hitModel and hitModel:FindFirstChildOfClass("Humanoid") then return true end
			return false
		end
		return true
	end

	local function detectSurvivor(): (Model?, Vector3?)
		local bestTarget: Model? = nil
		local bestDist = 65.0

		for _, pl in ipairs(Players:GetPlayers()) do
			local char = pl.Character
			if char and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0 then
				local hrp = char:FindFirstChild("HumanoidRootPart") :: BasePart?
				if hrp then
					local toPlayer = hrp.Position - root.Position
					local dist = toPlayer.Magnitude
					local isSprinting = char.Humanoid.WalkSpeed > 18.0

					local hearingRange = if isSprinting then 55.0 else 22.0
					local heard = (dist <= hearingRange)

					local seen = false
					if dist <= 50.0 then
						local dot = root.CFrame.LookVector:Dot(toPlayer.Unit)
						local angle = math.deg(math.acos(math.clamp(dot, -1, 1)))
						if angle <= 85.0 and hasLineOfSight(hrp.Position) then
							seen = true
						end
					end

					if (seen or heard) and dist < bestDist then
						bestDist = dist
						bestTarget = char
					end
				end
			end
		end

		if bestTarget and bestTarget:FindFirstChild("HumanoidRootPart") then
			return bestTarget, (bestTarget.HumanoidRootPart :: BasePart).Position
		end

		local alertPos = alertedPositions[zombie]
		if alertPos then
			alertedPositions[zombie] = nil
			return nil, alertPos
		end

		return nil, nil
	end

	-- Bucle de comportamiento autónomo
	task.spawn(function()
		while hum and hum.Health > 0 and zombie.Parent do
			local stunnedUntil = zombie:GetAttribute("StunnedUntil") or 0
			if os.clock() < stunnedUntil or hum.PlatformStand then
				hum.WalkSpeed = 0
				task.wait(0.2)
				continue
			end

			local targetChar, targetPos = detectSurvivor()

			if targetPos then
				local dist = (targetPos - root.Position).Magnitude

				if targetChar and dist <= 3.8 and os.clock() >= biteCooldown then
					biteCooldown = os.clock() + 1.25
					hum.WalkSpeed = 0
					isBiting = true

					local targetHum = targetChar:FindFirstChildOfClass("Humanoid")
					if targetHum and targetHum.Health > 0 then
						targetHum:TakeDamage(15.0)
						pcall(function() groanSound:Play() end)

						local roll = math.random(1, 100)
						local wound = if roll > 80 then "Mordida" elseif roll > 55 then "Laceración" else "Rasguño"
						local pl = Players:GetPlayerFromCharacter(targetChar)
						if pl then medicalRemote:FireClient(pl, "Damage", wound) end
					end
					task.wait(0.4)
					isBiting = false
				else
					hum.WalkSpeed = 8.5
					if hasLineOfSight(targetPos) then
						hum:MoveTo(targetPos)
					else
						local path = PathfindingService:CreatePath({
							AgentRadius = 2.0,
							AgentHeight = 5.0,
							AgentCanJump = false,
						})
						local ok = pcall(function() path:ComputeAsync(root.Position, targetPos) end)
						if ok and path.Status == Enum.PathStatus.Success then
							local waypoints = path:GetWaypoints()
							if #waypoints >= 2 then
								hum:MoveTo(waypoints[2].Position)
							else
								hum:MoveTo(targetPos)
							end
						else
							hum:MoveTo(targetPos)
						end
					end
				end
			else
				hum.WalkSpeed = 4.0
				local wander = spawnPos + Vector3.new(math.random(-12, 12), 0, math.random(-12, 12))
				hum:MoveTo(wander)
				if math.random(1, 8) == 1 then
					pcall(function() groanSound:Play() end)
				end
				task.wait(math.random(3, 5))
			end

			task.wait(0.35)
		end
	end)
end

--------------------------------------------------------------------------------
-- POBLACIÓN ESTRATÉGICA DE 35 ZOMBIS (TODOS EN Y = 3.5)
--------------------------------------------------------------------------------
local zombieFolder = Workspace:FindFirstChild("PZ_Zombies")
if not zombieFolder then
	zombieFolder = Instance.new("Folder")
	zombieFolder.Name = "PZ_Zombies"
	zombieFolder.Parent = Workspace
end

local function createZombieModel(name: string, spawnCFrame: CFrame): Model
	local m = Instance.new("Model")
	m.Name = name

	local root = Instance.new("Part")
	root.Name = "HumanoidRootPart"
	root.Size = Vector3.new(2, 2, 1)
	root.Transparency = 1
	root.CanCollide = true
	root.CFrame = spawnCFrame
	root.Parent = m

	local torso = Instance.new("Part")
	torso.Name = "Torso"
	torso.Size = Vector3.new(2, 2, 1)
	torso.Material = Enum.Material.Fabric
	torso.Color = Color3.fromRGB(55, 65, 55)
	torso.CanCollide = false
	torso.Parent = m

	local head = Instance.new("Part")
	head.Name = "Head"
	head.Size = Vector3.new(1.25, 1.25, 1.25)
	head.Material = Enum.Material.SmoothPlastic
	head.Color = Color3.fromRGB(115, 135, 110)
	head.CanCollide = false
	head.Parent = m

	local faceDecal = Instance.new("Decal")
	faceDecal.Name = "Face"
	faceDecal.Texture = "rbxasset://textures/face.png"
	faceDecal.Color3 = Color3.fromRGB(120, 140, 110)
	faceDecal.Face = Enum.NormalId.Front
	faceDecal.Parent = head

	local rArm = Instance.new("Part")
	rArm.Name = "Right Arm"
	rArm.Size = Vector3.new(1, 2, 1)
	rArm.Color = Color3.fromRGB(115, 135, 110)
	rArm.CanCollide = false
	rArm.Parent = m

	local lArm = Instance.new("Part")
	lArm.Name = "Left Arm"
	lArm.Size = Vector3.new(1, 2, 1)
	lArm.Color = Color3.fromRGB(115, 135, 110)
	lArm.CanCollide = false
	lArm.Parent = m

	local rLeg = Instance.new("Part")
	rLeg.Name = "Right Leg"
	rLeg.Size = Vector3.new(1, 2, 1)
	rLeg.Color = Color3.fromRGB(40, 42, 45)
	rLeg.CanCollide = false
	rLeg.Parent = m

	local lLeg = Instance.new("Part")
	lLeg.Name = "Left Leg"
	lLeg.Size = Vector3.new(1, 2, 1)
	lLeg.Color = Color3.fromRGB(40, 42, 45)
	lLeg.CanCollide = false
	lLeg.Parent = m

	local function makeMotor6D(p0: BasePart, p1: BasePart, c0: CFrame, c1: CFrame, motorName: string): Motor6D
		local m6 = Instance.new("Motor6D")
		m6.Name = motorName
		m6.Part0 = p0
		m6.Part1 = p1
		m6.C0 = c0
		m6.C1 = c1
		m6.Parent = p0
		return m6
	end

	makeMotor6D(root, torso, CFrame.new(0, 0, 0), CFrame.new(0, 0, 0), "RootJoint")
	makeMotor6D(torso, head, CFrame.new(0, 1, 0), CFrame.new(0, -0.5, 0), "Neck")
	makeMotor6D(torso, rArm, CFrame.new(1, 0.5, 0), CFrame.new(-0.5, 0.5, 0), "Right Shoulder")
	makeMotor6D(torso, lArm, CFrame.new(-1, 0.5, 0), CFrame.new(0.5, 0.5, 0), "Left Shoulder")
	makeMotor6D(torso, rLeg, CFrame.new(0.5, -1, 0), CFrame.new(0, 1, 0), "Right Hip")
	makeMotor6D(torso, lLeg, CFrame.new(-0.5, -1, 0), CFrame.new(0, 1, 0), "Left Hip")

	local hum = Instance.new("Humanoid")
	hum.MaxHealth = 100
	hum.Health = 100
	hum.WalkSpeed = 8.5
	hum.DisplayName = "Zombi Shambler"
	hum.Parent = m

	m.PrimaryPart = root
	m.Parent = zombieFolder
	return m
end

-- 35 Zombis en Rosewood todos con Y = 3.5 (Nivel de suelo limpio)
local zombieSpawns = {
	-- Comisaría (8)
	Vector3.new(-81.7, 3.5, 110.0), Vector3.new(-75.0, 3.5, 115.0),
	Vector3.new(-90.0, 3.5, 118.0), Vector3.new(-85.0, 3.5, 130.0),
	Vector3.new(-70.0, 3.5, 135.0), Vector3.new(-80.0, 3.5, 122.0),
	Vector3.new(-84.0, 3.5, 125.0), Vector3.new(-76.0, 3.5, 128.0),

	-- Estación de Bomberos (6)
	Vector3.new(110.9, 3.5, 185.0), Vector3.new(105.0, 3.5, 192.0),
	Vector3.new(118.0, 3.5, 195.0), Vector3.new(112.0, 3.5, 205.0),
	Vector3.new(108.0, 3.5, 202.0), Vector3.new(115.0, 3.5, 208.0),

	-- Calle Principal y Supermercado (6)
	Vector3.new(0.0, 3.5, -120.0), Vector3.new(15.0, 3.5, -140.0),
	Vector3.new(-20.0, 3.5, -160.0), Vector3.new(5.0, 3.5, -180.0),
	Vector3.new(-10.0, 3.5, -200.0), Vector3.new(20.0, 3.5, -220.0),

	-- Banco y Zona Comercial (4)
	Vector3.new(-57.3, 3.5, -210.0), Vector3.new(-52.0, 3.5, -218.0),
	Vector3.new(-62.0, 3.5, -225.0), Vector3.new(-70.0, 3.5, -230.0),

	-- Viviendas Residenciales y Patios (8)
	Vector3.new(180.0, 3.5, -220.0), Vector3.new(175.0, 3.5, -235.0),
	Vector3.new(190.0, 3.5, -240.0), Vector3.new(165.0, 3.5, -225.0),
	Vector3.new(155.0, 3.5, 15.0), Vector3.new(162.0, 3.5, 25.0),
	Vector3.new(150.0, 3.5, 35.0), Vector3.new(140.0, 3.5, 20.0),

	-- Parque y Callejones (3)
	Vector3.new(70.0, 3.5, -100.0), Vector3.new(85.0, 3.5, -120.0), Vector3.new(60.0, 3.5, -140.0),
}

for idx, pos in ipairs(zombieSpawns) do
	local cf = CFrame.new(pos) * CFrame.Angles(0, math.rad(math.random(0, 360)), 0)
	local z = createZombieModel("Zombi_Shambler_" .. idx, cf)
	setupZombieAI(z)
end

Workspace.DescendantAdded:Connect(function(desc)
	if desc:IsA("Model") and (desc.Name:find("Zombie") or desc.Name:find("Zombi")) then
		task.wait(0.3)
		setupZombieAI(desc)
	end
end)
