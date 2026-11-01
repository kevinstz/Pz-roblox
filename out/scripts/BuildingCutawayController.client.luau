--!strict
-- BuildingCutawayController.client.luau
-- MÓDULO 3.2: Oclusión Dinámica Multicapa (Cutaway 2.0) y Raycast Cutaway de Muros
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local player = Players.LocalPlayer
local camera = Workspace.CurrentCamera

type BuildingFloorData = {
	model: Model,
	boundsMinX: number, boundsMaxX: number,
	boundsMinZ: number, boundsMaxZ: number,
	baseY: number,
	piso0Parts: { BasePart },
	upperParts: { BasePart }, -- Piso_1, Piso_2, etc.
	piso2PlusParts: { BasePart }, -- Piso_2, Piso_3, etc.
	roofParts: { BasePart },
	wallParts: { BasePart },
}

local buildings: { BuildingFloorData } = {}
local isReady = false
local currentTransparency: { [BasePart]: number } = {}
local raycastParams = RaycastParams.new()
raycastParams.FilterType = Enum.RaycastFilterType.Exclude

local function scanBuildings()
	buildings = {}
	local map = Workspace:FindFirstChild("PZ_Rosewood_B42")
	if not map then return end
	local edifFolder = map:FindFirstChild("Edificios")
	if not edifFolder then return end

	for _, bld in ipairs(edifFolder:GetChildren()) do
		if bld:IsA("Model") then
			local bData: BuildingFloorData = {
				model = bld,
				boundsMinX = Infinity, boundsMaxX = -Infinity,
				boundsMinZ = Infinity, boundsMaxZ = -Infinity,
				baseY = 0,
				piso0Parts = {},
				upperParts = {},
				piso2PlusParts = {},
				roofParts = {},
				wallParts = {},
			}

			local ok, cf, sz = pcall(function() return bld:GetBoundingBox() end)
			if ok and cf and sz then
				bData.boundsMinX = cf.Position.X - (sz.X * 0.5) - 1.5
				bData.boundsMaxX = cf.Position.X + (sz.X * 0.5) + 1.5
				bData.boundsMinZ = cf.Position.Z - (sz.Z * 0.5) - 1.5
				bData.boundsMaxZ = cf.Position.Z + (sz.Z * 0.5) + 1.5
				bData.baseY = cf.Position.Y - (sz.Y * 0.5)
			end

			for _, desc in ipairs(bld:GetDescendants()) do
				if desc:IsA("BasePart") then
					local parent = desc.Parent
					local pName = if parent then parent.Name else ""
					local nLower = string.lower(desc.Name)

					if nLower:find("techo") or nLower:find("roof") then
						table.insert(bData.roofParts, desc)
					elseif pName == "Piso_0" or pName == "Piso_-1" then
						table.insert(bData.piso0Parts, desc)
					elseif pName == "Piso_1" then
						table.insert(bData.upperParts, desc)
					elseif pName:find("Piso_") then
						table.insert(bData.upperParts, desc)
						table.insert(bData.piso2PlusParts, desc)
					end

					if nLower:find("walls_") or nLower:find("pared") or nLower:find("puerta") or nLower:find("window") then
						table.insert(bData.wallParts, desc)
					end
				end
			end

			table.insert(buildings, bData)
		end
	end
	isReady = true
end

local lastCutawayCheck = 0

RunService.RenderStepped:Connect(function()
	if not isReady then
		scanBuildings()
		if not isReady then return end
	end

	local char = player.Character
	if not char then return end
	local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end

	local now = os.clock()
	if now - lastCutawayCheck < 0.033 then return end -- 30 Hz
	lastCutawayCheck = now

	local pPos = root.Position
	local activeBld: BuildingFloorData? = nil

	for _, b in ipairs(buildings) do
		if pPos.X >= b.boundsMinX and pPos.X <= b.boundsMaxX and
		   pPos.Z >= b.boundsMinZ and pPos.Z <= b.boundsMaxZ then
			activeBld = b
			break
		end
	end

	local desiredTransparency: { [BasePart]: number } = {}

	if activeBld then
		-- JUGADOR DENTRO DE UN EDIFICIO
		local relativeY = pPos.Y - activeBld.baseY

		if relativeY < 12.0 then
			-- En Piso 0: ocultar todos los pisos superiores y techos
			for _, part in ipairs(activeBld.upperParts) do
				desiredTransparency[part] = 1.0
			end
			for _, part in ipairs(activeBld.roofParts) do
				desiredTransparency[part] = 1.0
			end
		else
			-- En Piso 1+: Piso 1 visible, ocultar Piso 2+ y techo
			for _, part in ipairs(activeBld.piso2PlusParts) do
				desiredTransparency[part] = 1.0
			end
			for _, part in ipairs(activeBld.roofParts) do
				desiredTransparency[part] = 1.0
			end
		end

		-- OCLUSIÓN DE MUROS MEDIANTE 5 RAYCASTS (Cabeza, Torso, Caderas, Pie Izq, Pie Der)
		raycastParams.FilterDescendantsInstances = { char }
		local camPos = camera.CFrame.Position
		local targets = {
			pPos + Vector3.new(0, 1.8, 0), -- Cabeza
			pPos + Vector3.new(0, 0.9, 0), -- Torso
			pPos,                          -- Caderas
			pPos + Vector3.new(-0.8, -1.2, 0), -- Pie Izq
			pPos + Vector3.new(0.8, -1.2, 0),  -- Pie Der
		}

		for _, tPos in ipairs(targets) do
			local dir = tPos - camPos
			local hit = Workspace:Raycast(camPos, dir, raycastParams)
			if hit and hit.Instance and hit.Instance:IsA("BasePart") then
				local hPart = hit.Instance
				local hName = string.lower(hPart.Name)
				if hName:find("wall") or hName:find("pared") or hName:find("door") or hName:find("puerta") then
					desiredTransparency[hPart] = 0.85 -- Opacidad suave
				end
			end
		end
	end

	-- Aplicar transparencias diferenciales eficientes
	for part, oldT in pairs(currentTransparency) do
		local newT = desiredTransparency[part] or 0.0
		if newT ~= oldT then
			part.LocalTransparencyModifier = newT
			if newT == 0.0 then
				currentTransparency[part] = nil
			else
				currentTransparency[part] = newT
			end
		end
	end

	for part, newT in pairs(desiredTransparency) do
		if currentTransparency[part] ~= newT then
			part.LocalTransparencyModifier = newT
			currentTransparency[part] = newT
		end
	end
end)
