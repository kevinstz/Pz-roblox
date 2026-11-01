--!strict
-- IsometricCamera.client.luau
-- MÓDULO 3.1: Cámara Isométrica Inmediata de Project Zomboid Build 42 (FOV 22, Cero Lag)
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")

local localPlayer = Players.LocalPlayer
local camera = Workspace.CurrentCamera

local BASE_DISTANCE = 70.0
local MIN_DISTANCE = 45.0
local MAX_DISTANCE = 110.0
local BASE_FOV = 22.0

local targetDistance = BASE_DISTANCE
local currentDistance = BASE_DISTANCE
local isAiming = false
local aimOffset = Vector3.zero

-- 1. ZOOM INMEDIATO CON RUEDA DEL RATÓN
UserInputService.InputChanged:Connect(function(input: InputObject, processed: boolean)
	if processed then return end
	if input.UserInputType == Enum.UserInputType.MouseWheel then
		targetDistance = math.clamp(targetDistance - (input.Position.Z * 7.0), MIN_DISTANCE, MAX_DISTANCE)
	end
end)

UserInputService.InputBegan:Connect(function(input: InputObject, processed: boolean)
	if processed then return end
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = true
	end
end)

UserInputService.InputEnded:Connect(function(input: InputObject, processed: boolean)
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = false
		aimOffset = Vector3.zero
	end
end)

-- 2. FIJADO INMEDIATO DE CÁMARA (CERO SEGUNDOS MIRANDO AL CIELO)
local function onRenderCamera(dt: number)
	local character = localPlayer.Character
	if not character then return end
	local rootPart = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not rootPart then return end

	-- Fija el tipo de cámara en el primer frame
	camera.CameraType = Enum.CameraType.Scriptable
	camera.FieldOfView = BASE_FOV

	-- Suavizado de zoom
	currentDistance += (targetDistance - currentDistance) * math.clamp(dt * 14.0, 0, 1)

	-- Look-ahead táctico al apuntar con RMB
	if isAiming then
		local mouseLoc = UserInputService:GetMouseLocation()
		local ray = camera:ViewportPointToRay(mouseLoc.X, mouseLoc.Y)
		local groundY = rootPart.Position.Y
		local t = (groundY - ray.Origin.Y) / ray.Direction.Y
		if t > 0 then
			local hitPos = ray.Origin + ray.Direction * t
			local delta = hitPos - rootPart.Position
			local flatDelta = Vector3.new(delta.X, 0, delta.Z)
			if flatDelta.Magnitude > 0.5 then
				local desiredOffset = flatDelta.Unit * math.min(flatDelta.Magnitude * 0.35, 18.0)
				aimOffset = aimOffset:Lerp(desiredOffset, dt * 8.0)
			end
		end
	else
		aimOffset = aimOffset:Lerp(Vector3.zero, dt * 8.0)
	end

	local focusPos = rootPart.Position + aimOffset + Vector3.new(0, 1.8, 0)
	-- Offset exacto isométrico 65, 75, 65 normalizado escalado por la distancia
	local isoOffset = Vector3.new(1, 1.15, 1).Unit * currentDistance
	local camPos = focusPos + isoOffset

	camera.CFrame = CFrame.lookAt(camPos, focusPos)
end

RunService:BindToRenderStep("PZ_IsometricCamera", Enum.RenderPriority.Camera.Value + 1, onRenderCamera)
