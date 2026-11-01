def format_suelo_part(name, cx, cy, cz, sx, sy, sz, color_rgb, material_token, ref_part, ref_tex, uid_part, uid_tex, tex_url):
    r, g, b = color_rgb
    c_uint32 = 0xFF000000 | (r << 16) | (g << 8) | b
    
    return f"""\t\t\t\t\t<Item class="Part" referent="R{ref_part}">
\t\t\t\t\t\t<Properties>
\t\t\t\t\t\t\t<token name="shape">1</token>
\t\t\t\t\t\t\t<token name="formFactorRaw">1</token>
\t\t\t\t\t\t\t<bool name="Anchored">true</bool>
\t\t\t\t\t\t\t<bool name="AudioCanCollide">true</bool>
\t\t\t\t\t\t\t<float name="BackParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="BackParamB">0.5</float>
\t\t\t\t\t\t\t<token name="BackSurface">0</token>
\t\t\t\t\t\t\t<token name="BackSurfaceInput">0</token>
\t\t\t\t\t\t\t<float name="BottomParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="BottomParamB">0.5</float>
\t\t\t\t\t\t\t<token name="BottomSurface">0</token>
\t\t\t\t\t\t\t<token name="BottomSurfaceInput">0</token>
\t\t\t\t\t\t\t<CoordinateFrame name="CFrame">
\t\t\t\t\t\t\t\t<X>{cx}</X>
\t\t\t\t\t\t\t\t<Y>{cy}</Y>
\t\t\t\t\t\t\t\t<Z>{cz}</Z>
\t\t\t\t\t\t\t\t<R00>1</R00>
\t\t\t\t\t\t\t\t<R01>0</R01>
\t\t\t\t\t\t\t\t<R02>0</R02>
\t\t\t\t\t\t\t\t<R10>0</R10>
\t\t\t\t\t\t\t\t<R11>1</R11>
\t\t\t\t\t\t\t\t<R12>0</R12>
\t\t\t\t\t\t\t\t<R20>0</R20>
\t\t\t\t\t\t\t\t<R21>0</R21>
\t\t\t\t\t\t\t\t<R22>1</R22>
\t\t\t\t\t\t\t</CoordinateFrame>
\t\t\t\t\t\t\t<bool name="CanCollide">true</bool>
\t\t\t\t\t\t\t<bool name="CanQuery">true</bool>
\t\t\t\t\t\t\t<bool name="CanTouch">true</bool>
\t\t\t\t\t\t\t<bool name="CastShadow">true</bool>
\t\t\t\t\t\t\t<string name="CollisionGroup">Default</string>
\t\t\t\t\t\t\t<int name="CollisionGroupId">0</int>
\t\t\t\t\t\t\t<Color3uint8 name="Color3uint8">{c_uint32}</Color3uint8>
\t\t\t\t\t\t\t<PhysicalProperties name="CustomPhysicalProperties">
\t\t\t\t\t\t\t\t<CustomPhysics>false</CustomPhysics>
\t\t\t\t\t\t\t</PhysicalProperties>
\t\t\t\t\t\t\t<bool name="EnableFluidForces">true</bool>
\t\t\t\t\t\t\t<float name="FrontParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="FrontParamB">0.5</float>
\t\t\t\t\t\t\t<token name="FrontSurface">0</token>
\t\t\t\t\t\t\t<token name="FrontSurfaceInput">0</token>
\t\t\t\t\t\t\t<float name="LeftParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="LeftParamB">0.5</float>
\t\t\t\t\t\t\t<token name="LeftSurface">0</token>
\t\t\t\t\t\t\t<token name="LeftSurfaceInput">0</token>
\t\t\t\t\t\t\t<bool name="Locked">false</bool>
\t\t\t\t\t\t\t<bool name="Massless">false</bool>
\t\t\t\t\t\t\t<token name="Material">{material_token}</token>
\t\t\t\t\t\t\t<string name="MaterialVariantSerialized"></string>
\t\t\t\t\t\t\t<CoordinateFrame name="PivotOffset">
\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t\t<R00>1</R00>
\t\t\t\t\t\t\t\t<R01>0</R01>
\t\t\t\t\t\t\t\t<R02>0</R02>
\t\t\t\t\t\t\t\t<R10>0</R10>
\t\t\t\t\t\t\t\t<R11>1</R11>
\t\t\t\t\t\t\t\t<R12>0</R12>
\t\t\t\t\t\t\t\t<R20>0</R20>
\t\t\t\t\t\t\t\t<R21>0</R21>
\t\t\t\t\t\t\t\t<R22>1</R22>
\t\t\t\t\t\t\t</CoordinateFrame>
\t\t\t\t\t\t\t<float name="Reflectance">0</float>
\t\t\t\t\t\t\t<float name="RightParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="RightParamB">0.5</float>
\t\t\t\t\t\t\t<token name="RightSurface">0</token>
\t\t\t\t\t\t\t<token name="RightSurfaceInput">0</token>
\t\t\t\t\t\t\t<int name="RootPriority">0</int>
\t\t\t\t\t\t\t<Vector3 name="RotVelocity">
\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t<float name="TopParamA">-0.5</float>
\t\t\t\t\t\t\t<float name="TopParamB">0.5</float>
\t\t\t\t\t\t\t<token name="TopSurface">0</token>
\t\t\t\t\t\t\t<token name="TopSurfaceInput">0</token>
\t\t\t\t\t\t\t<float name="Transparency">0</float>
\t\t\t\t\t\t\t<Vector3 name="Velocity">
\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t<Z>0</Z>
\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t<Vector3 name="size">
\t\t\t\t\t\t\t\t<X>{sx}</X>
\t\t\t\t\t\t\t\t<Y>{sy}</Y>
\t\t\t\t\t\t\t\t<Z>{sz}</Z>
\t\t\t\t\t\t\t</Vector3>
\t\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>
\t\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>
\t\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>
\t\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>
\t\t\t\t\t\t\t<string name="Name">{name}</string>
\t\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>
\t\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>
\t\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>
\t\t\t\t\t\t\t<UniqueId name="UniqueId">{uid_part}</UniqueId>
\t\t\t\t\t\t</Properties>
\t\t\t\t\t\t<Item class="Texture" referent="R{ref_tex}">
\t\t\t\t\t\t\t<Properties>
\t\t\t\t\t\t\t\t<float name="OffsetStudsU">0</float>
\t\t\t\t\t\t\t\t<float name="OffsetStudsV">0</float>
\t\t\t\t\t\t\t\t<float name="StudsPerTileU">3</float>
\t\t\t\t\t\t\t\t<float name="StudsPerTileV">3</float>
\t\t\t\t\t\t\t\t<bool name="AutoLocalize">true</bool>
\t\t\t\t\t\t\t\t<Color3 name="Color3">
\t\t\t\t\t\t\t\t\t<R>1</R>
\t\t\t\t\t\t\t\t\t<G>1</G>
\t\t\t\t\t\t\t\t\t<B>1</B>
\t\t\t\t\t\t\t\t</Color3>
\t\t\t\t\t\t\t\t<Content name="EmissiveMaskContent">
\t\t\t\t\t\t\t\t\t<null></null>
\t\t\t\t\t\t\t\t</Content>
\t\t\t\t\t\t\t\t<float name="EmissiveStrength">1</float>
\t\t\t\t\t\t\t\t<Color3 name="EmissiveTint">
\t\t\t\t\t\t\t\t\t<R>1</R>
\t\t\t\t\t\t\t\t\t<G>1</G>
\t\t\t\t\t\t\t\t\t<B>1</B>
\t\t\t\t\t\t\t\t</Color3>
\t\t\t\t\t\t\t\t<Content name="MetalnessMap"><null></null></Content>
\t\t\t\t\t\t\t\t<Content name="NormalMap"><null></null></Content>
\t\t\t\t\t\t\t\t<token name="ResampleMode">0</token>
\t\t\t\t\t\t\t\t<float name="Rotation">0</float>
\t\t\t\t\t\t\t\t<Content name="RoughnessMap"><null></null></Content>
\t\t\t\t\t\t\t\t<Content name="Texture"><url>{tex_url}</url></Content>
\t\t\t\t\t\t\t\t<Content name="TexturePack"><null></null></Content>
\t\t\t\t\t\t\t\t<string name="TexturePackMetadata"></string>
\t\t\t\t\t\t\t\t<float name="Transparency">0</float>
\t\t\t\t\t\t\t\t<Vector2 name="UVOffset">
\t\t\t\t\t\t\t\t\t<X>0</X>
\t\t\t\t\t\t\t\t\t<Y>0</Y>
\t\t\t\t\t\t\t\t</Vector2>
\t\t\t\t\t\t\t\t<Vector2 name="UVScale">
\t\t\t\t\t\t\t\t\t<X>1</X>
\t\t\t\t\t\t\t\t\t<Y>1</Y>
\t\t\t\t\t\t\t\t</Vector2>
\t\t\t\t\t\t\t\t<int name="ZIndex">1</int>
\t\t\t\t\t\t\t\t<token name="Face">1</token>
\t\t\t\t\t\t\t\t<BinaryString name="AttributesSerialize"></BinaryString>
\t\t\t\t\t\t\t\t<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>
\t\t\t\t\t\t\t\t<bool name="DefinesCapabilities">false</bool>
\t\t\t\t\t\t\t\t<UniqueId name="HistoryId">00000000000000000000000000000000</UniqueId>
\t\t\t\t\t\t\t\t<string name="Name">Texture</string>
\t\t\t\t\t\t\t\t<BinaryString name="SerializedOverrides"></BinaryString>
\t\t\t\t\t\t\t\t<int64 name="SourceAssetId">-1</int64>
\t\t\t\t\t\t\t\t<SharedString name="Tags">yuZpQdnvvUBOTYh1jqZ2cA==</SharedString>
\t\t\t\t\t\t\t\t<UniqueId name="UniqueId">{uid_tex}</UniqueId>
\t\t\t\t\t\t\t</Properties>
\t\t\t\t\t\t</Item>
\t\t\t\t\t</Item>\n"""

print("Part template loaded successfully.")
