--!strict
-- WorldAtmosphereController.server.luau
-- MÓDULO 1.3: Farolas Realistas (1.5x0.4x0.8) con SpotLight Nocturno (19:00) y Depuración de Interiores
local Lighting = game:GetService("Lighting")
local Workspace = game:GetService("Workspace")

local streetlights: { { light: SpotLight, bulb: BasePart } } = {}

-- Bounding boxes de los 14 edificios para evitar farolas dentro de paredes o habitaciones
local buildingBounds = {
	{ minX = -86.0, maxX = -28.0, minZ = -262.0, maxZ = -174.0 }, -- Banco
	{ minX = 39.0, maxX = 109.0, minZ = -192.0, maxZ = -156.0 },  -- Derelict 5
	{ minX = 57.0, maxX = 83.0, minZ = 0.0, maxZ = 27.0 },        -- Chinese Kitchen
	{ minX = -165.0, maxX = -111.0, minZ = -252.0, maxZ = -198.0 }, -- Cafe
	{ minX = -99.0, maxX = -18.0, minZ = -252.0, maxZ = -214.0 },  -- Office 9
	{ minX = 38.0, maxX = 123.0, minZ = -252.0, maxZ = -78.0 },   -- Libreria
	{ minX = 175.0, maxX = 189.0, minZ = -249.0, maxZ = -218.0 }, -- Livingroom 28
	{ minX = -114.0, maxX = -19.0, minZ = -210.0, maxZ = -153.0 }, -- Office 8
	{ minX = 104.0, maxX = 117.0, minZ = -177.0, maxZ = -159.0 }, -- Derelict 22
	{ minX = -153.0, maxX = -46.0, minZ = -90.0, maxZ = 33.0 },    -- Bar
	{ minX = 39.0, maxX = 112.0, minZ = -33.0, maxZ = 78.0 },     -- Office 24
	{ minX = 146.0, maxX = 168.0, minZ = 9.0, maxZ = 39.0 },      -- Livingroom 33
	{ minX = -165.0, maxX = -37.0, minZ = 146.0, maxZ = 249.0 },  -- Comisaria
	{ minX = 57.0, maxX = 167.0, minZ = 160.0, maxZ = 237.0 },    -- Bomberos
}

local function isInsideBuilding(pos: Vector3): boolean
	for _, b in ipairs(buildingBounds) do
		if pos.X >= b.minX and pos.X <= b.maxX and pos.Z >= b.minZ and pos.Z <= b.maxZ then
			return true
		end
	end
	return false
end

local function setupStreetlight(part: BasePart)
	local nameLower = string.lower(part.Name)
	if nameLower:find("lighting_outdoor_") or nameLower:find("street_decoration_") then
		local pos = part.Position

		-- Eliminar farolas invasivas dentro de edificios
		if isInsideBuilding(pos) then
			part:Destroy()
			return
		end

		if part.Size.Y > 5.0 or nameLower:find("post") or nameLower:find("lighting_outdoor_01_2") then
			part.Shape = Enum.PartType.Cylinder
			part.Size = Vector3.new(12.0, 0.5, 0.5)
			part.Material = Enum.Material.Metal
			part.Color = Color3.fromRGB(42, 45, 48)
			part.CanCollide = true

			local bulb = part:FindFirstChild("StreetBulb") :: BasePart?
			if not bulb then
				bulb = Instance.new("Part")
				bulb.Name = "StreetBulb"
				bulb.Shape = Enum.PartType.Block
				bulb.Size = Vector3.new(1.5, 0.4, 0.8) -- Tamaño realista MÓDULO 1.3
				bulb.Material = Enum.Material.Glass
				bulb.Color = Color3.fromRGB(255, 230, 160)
				bulb.Anchored = true
				bulb.CanCollide = false
				bulb.CFrame = part.CFrame * CFrame.new(0, 5.8, 1.2)
				bulb.Parent = part
			else
				bulb.Size = Vector3.new(1.5, 0.4, 0.8)
			end

			local spot = bulb:FindFirstChildOfClass("SpotLight") or Instance.new("SpotLight")
			spot.Name = "StreetSpot"
			spot.Face = Enum.NormalId.Bottom
			spot.Angle = 75
			spot.Range = 35
			spot.Brightness = 2.8
			spot.Color = Color3.fromRGB(255, 225, 160)
			spot.Shadows = true
			spot.Enabled = false
			spot.Parent = bulb

			table.insert(streetlights, { light = spot, bulb = bulb })
		end
	end
end

local function updateStreetlights()
	local clock = Lighting.ClockTime
	local isNight = (clock >= 19.0 or clock < 6.0)
	for _, sl in ipairs(streetlights) do
		sl.light.Enabled = isNight
		sl.bulb.Material = if isNight then Enum.Material.Neon else Enum.Material.Glass
	end
end

Lighting:GetPropertyChangedSignal("ClockTime"):Connect(updateStreetlights)

for _, desc in ipairs(Workspace:GetDescendants()) do
	if desc:IsA("BasePart") then setupStreetlight(desc) end
end

updateStreetlights()
