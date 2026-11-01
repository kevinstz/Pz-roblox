import os
import shutil

src = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
bak = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_before_motion_fix"
dst_tmp = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.tmp"

print("1. Creating safety backup...")
if not os.path.exists(bak):
    shutil.copyfile(src, bak)
    print("Backup created at:", bak)
else:
    print("Backup already exists.")

NEW_CAMERA_SOURCE = """--!strict
--[[
	Cámara Isométrica extraída directamente de ProjectZomboidRoblox.rbxlx
	- Parámetros exactos de Project Zomboid (Pitch -30°, Yaw 45°, Distancia 115, FOV 13.5 teleobjetivo)
	- Zoom en rueda de ratón (FOV entre 7.5° y 24.0°)
	- Apuntado con Click Derecho (RMB) y seguimiento de cursor sobre el plano del suelo con look-ahead
	- Sincronización continua de Camera.Focus y RenderPriority.Camera.Value + 1 para evitar culling en movimiento
]]

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")

local localPlayer = Players.LocalPlayer
local camera = Workspace.CurrentCamera

-- Parámetros de cámara isométrica clásica de Project Zomboid
local ISO_PITCH_DEG = -30.0
local ISO_YAW_DEG = 45.0
local CAMERA_DISTANCE = 115.0
local BASE_FOV = 13.5
local MIN_ZOOM_FOV = 7.5
local MAX_ZOOM_FOV = 24.0

local currentFov = BASE_FOV
local isAiming = false
local aimCursorLookOffset = Vector3.zero

-- Controles de Teclado y Ratón
UserInputService.InputChanged:Connect(function(input: InputObject, gameProcessed: boolean)
	if gameProcessed then
		return
	end
	if input.UserInputType == Enum.UserInputType.MouseWheel then
		currentFov = math.clamp(currentFov - (input.Position.Z * 1.4), MIN_ZOOM_FOV, MAX_ZOOM_FOV)
	end
end)

UserInputService.InputBegan:Connect(function(input: InputObject, gameProcessed: boolean)
	if gameProcessed then
		return
	end
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = true
	end
end)

UserInputService.InputEnded:Connect(function(input: InputObject, gameProcessed: boolean)
	if input.UserInputType == Enum.UserInputType.MouseButton2 then
		isAiming = false
		aimCursorLookOffset = Vector3.zero
	end
end)

-- Bucle por frame: Sincronización de Cámara Isométrica y Focus de Renderizado
RunService:BindToRenderStep("PZ_IsometricCamera", Enum.RenderPriority.Camera.Value + 1, function(dt: number)
	local character = localPlayer.Character
	if not character then
		return
	end
	local rootPart = character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not rootPart then
		return
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")

	camera.CameraType = Enum.CameraType.Scriptable
	camera.FieldOfView = currentFov
	if humanoid then
		camera.CameraSubject = humanoid
	end

	if isAiming then
		local mouseLoc = UserInputService:GetMouseLocation()
		local unitRay = camera:ViewportPointToRay(mouseLoc.X, mouseLoc.Y)
		local groundPlaneY = rootPart.Position.Y
		local t = (groundPlaneY - unitRay.Origin.Y) / unitRay.Direction.Y
		if t > 0 then
			local hitPos = unitRay.Origin + unitRay.Direction * t
			local delta = hitPos - rootPart.Position
			local flatDir = Vector3.new(delta.X, 0, delta.Z)
			if flatDir.Magnitude > 0.1 then
				aimCursorLookOffset = aimCursorLookOffset:Lerp(flatDir.Unit * math.min(flatDir.Magnitude * 0.24, 18.0), dt * 6.0)
			end
		end
	else
		aimCursorLookOffset = aimCursorLookOffset:Lerp(Vector3.zero, dt * 6.0)
	end

	local focusPos = rootPart.Position + aimCursorLookOffset
	local isoRotation = CFrame.Angles(0, math.rad(ISO_YAW_DEG), 0) * CFrame.Angles(math.rad(ISO_PITCH_DEG), 0, 0)
	local camPos = focusPos - (isoRotation.LookVector * CAMERA_DISTANCE)

	camera.Focus = CFrame.new(focusPos)
	camera.CFrame = CFrame.lookAt(camPos, focusPos)
end)"""

print("2. Streaming processing PZ_Rosewood.rbxlx...")
chunks_mode_updated = 0
camera_script_updated = False
terreno_y_updated = False

in_suelo0 = False
in_iso_camera = False
in_iso_source = False

with open(src, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(dst_tmp, "w", encoding="utf-8") as f_out:
    
    for line in f_in:
        # Track Suelo_Piso_0 boundaries
        if 'name="Name">Suelo_Piso_0<' in line:
            in_suelo0 = True
        elif in_suelo0 and ('referent="R33263"' in line or 'name="Name">Suelo_Piso_1<' in line):
            in_suelo0 = False

        # In Suelo_Piso_0, update ModelStreamingMode from 0 to 2 for chunks
        if in_suelo0 and '<token name="ModelStreamingMode">0</token>' in line:
            line = line.replace('<token name="ModelStreamingMode">0</token>', '<token name="ModelStreamingMode">2</token>')
            chunks_mode_updated += 1

        # Track IsometricCamera LocalScript (referent="R153412")
        if 'referent="R153412"' in line:
            in_iso_camera = True
        
        if in_iso_camera:
            if '<ProtectedString name="Source"><![CDATA[' in line:
                in_iso_source = True
                f_out.write('\t\t\t\t\t<ProtectedString name="Source"><![CDATA[' + NEW_CAMERA_SOURCE + ']]></ProtectedString>\n')
                camera_script_updated = True
                continue
            if in_iso_source:
                if ']]></ProtectedString>' in line:
                    in_iso_source = False
                continue
            if '</Item>' in line:
                in_iso_camera = False

        # TerrenoCircundante CFrame Y adjustment (-3.2 -> -4.0)
        if '<Y>-3.2</Y>' in line:
            line = line.replace('<Y>-3.2</Y>', '<Y>-4.0</Y>')
            terreno_y_updated = True

        f_out.write(line)

print(f"Chunks updated to Persistent (2): {chunks_mode_updated}")
print(f"Camera script updated: {camera_script_updated}")
print(f"TerrenoCircundante Y updated: {terreno_y_updated}")

assert chunks_mode_updated == 88, f"Expected 88 chunks updated, got {chunks_mode_updated}"
assert camera_script_updated, "Camera script was not updated!"
assert terreno_y_updated, "TerrenoCircundante Y was not updated!"

print("Replacing original with tmp file...")
os.replace(dst_tmp, src)
print("Replacement complete successfully!")
