import os
import shutil
import re
import uuid
import numpy as np
from generate_house_upgrades import (
    HouseUpgradeBuilder, R_ID, R_FALL_EAST, R_FALL_WEST,
    R_GABLE_RISE_EAST, R_GABLE_RISE_WEST,
    TEX_ROOF_DARK, TEX_ROOF_TAN, TEX_SIDING, TEX_SKIRTING,
    TEX_WOOD_DECK, TEX_AC_GRILL
)

RBXLX_PATH = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx"
BACKUP_PATH = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.bak_houses"
TEMP_OUT = r"C:\Users\julia\.gemini\antigravity\scratch\pz_roblox_b42\out\PZ_Rosewood.rbxlx.tmp"

print("1. Creating backup of PZ_Rosewood.rbxlx...")
if not os.path.exists(BACKUP_PATH):
    shutil.copy2(RBXLX_PATH, BACKUP_PATH)
    print("  Backup created successfully.")
else:
    print("  Backup already exists.")

builder = HouseUpgradeBuilder(start_ref=200000)

def build_house_28():
    # Livingroom_31_45_28 (Baby Blue / Slate Blue)
    piso_0 = []
    
    # Skirting (Zócalo de Bloques de Cemento)
    piso_0.append(builder.part("skirting_west", (178.42, 0.35, -234.00), R_ID, (0.30, 1.70, 27.20),
                               color=(120, 122, 125), material="Concrete",
                               textures=[("Left", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_east", (187.58, 0.35, -234.00), R_ID, (0.30, 1.70, 27.20),
                               color=(120, 122, 125), material="Concrete",
                               textures=[("Right", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_north", (183.00, 0.35, -247.58), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete",
                               textures=[("Back", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_south", (183.00, 0.35, -220.35), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete",
                               textures=[("Front", TEX_SKIRTING, 3, 1.5)]))
                               
    # Front Porch Deck (West side at door X=178.63, Z=-236.87)
    piso_0.append(builder.part("porch_deck", (176.50, 1.20, -236.87), R_ID, (4.00, 0.30, 5.50),
                               color=(130, 85, 50), material="WoodPlanks",
                               textures=[("Top", TEX_WOOD_DECK, 2, 2)]))
    # Posts under deck
    for px, pz in [(174.65, -239.40), (174.65, -234.34), (178.35, -239.40), (178.35, -234.34)]:
        piso_0.append(builder.part("porch_post", (px, 0.45, pz), R_ID, (0.25, 1.50, 0.25),
                                   color=(110, 70, 40), material="Wood"))
    # Steps
    piso_0.append(builder.part("porch_step_1", (173.90, 0.80, -236.87), R_ID, (1.20, 0.30, 3.50),
                               color=(130, 85, 50), material="WoodPlanks"))
    piso_0.append(builder.part("porch_step_2", (172.70, 0.40, -236.87), R_ID, (1.20, 0.30, 3.50),
                               color=(130, 85, 50), material="WoodPlanks"))
    # Railings (North & South sides)
    for rz, rname in [(-239.50, "north"), (-234.24, "south")]:
        piso_0.append(builder.part(f"porch_rail_top_{rname}", (176.50, 2.75, rz), R_ID, (4.00, 0.18, 0.18),
                                   color=(245, 245, 248), material="Wood"))
        piso_0.append(builder.part(f"porch_rail_bot_{rname}", (176.50, 1.45, rz), R_ID, (4.00, 0.15, 0.15),
                                   color=(245, 245, 248), material="Wood"))
        for rx in [174.8, 175.9, 177.0, 178.1]:
            piso_0.append(builder.part(f"porch_spindle_{rname}", (rx, 2.10, rz), R_ID, (0.12, 1.20, 0.12),
                                       color=(245, 245, 248), material="Wood"))

    # Window AC Unit (on West window at X=178.68, Z=-230.87, Y=4.30)
    piso_0.append(builder.part("ac_unit_casing", (177.55, 4.30, -230.87), R_ID, (1.80, 1.30, 1.80),
                               color=(215, 218, 220), material="SmoothPlastic",
                               textures=[("Left", TEX_AC_GRILL, 1.8, 1.3)]))
    piso_0.append(builder.part("ac_bracket_1", (178.00, 3.40, -231.50), R_ID, (0.80, 0.10, 0.10),
                               color=(100, 105, 110), material="Metal"))
    piso_0.append(builder.part("ac_bracket_2", (178.00, 3.40, -230.24), R_ID, (0.80, 0.10, 0.10),
                               color=(100, 105, 110), material="Metal"))

    # Porch Sconce Lamp (West wall next to door at X=178.45, Z=-239.00, Y=4.50)
    piso_0.append(builder.part("porch_sconce", (178.45, 4.50, -239.00), R_ID, (0.25, 0.60, 0.25),
                               color=(30, 32, 35), material="Metal"))
    piso_0.append(builder.part("porch_light_bulb", (178.25, 4.45, -239.00), R_ID, (0.20, 0.20, 0.20),
                               color=(255, 235, 170), material="Glass",
                               point_light=(1.2, 16.0, (1.0, 0.88, 0.65))))

    # Piso_1 elements (Gabled roof, ridge cap, gable walls, TV antenna, interior ceiling)
    piso_1 = [builder.model_open("Piso_1")]
    
    # Interior flat ceiling slab (now in Piso_1 so it cuts away when inside!)
    piso_1.append(builder.part("roofs_interior_ceiling_main", (183.00, 7.30, -235.50), R_ID, (9.00, 0.20, 24.00),
                               color=(210, 210, 210), material="SmoothPlastic"))
    piso_1.append(builder.part("roofs_interior_ceiling_end", (186.00, 7.30, -222.00), R_ID, (3.00, 0.20, 3.00),
                               color=(210, 210, 210), material="SmoothPlastic"))

    # West Roof Slope (falling to -X)
    piso_1.append(builder.part("roofs_slope_west", (180.45, 8.475, -234.00), R_FALL_WEST, (28.00, 2.25, 5.10),
                               color=(48, 52, 58), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_DARK, 3, 3)]))
    # East Roof Slope (falling to +X)
    piso_1.append(builder.part("roofs_slope_east", (185.55, 8.475, -234.00), R_FALL_EAST, (28.00, 2.25, 5.10),
                               color=(48, 52, 58), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_DARK, 3, 3)]))
    # Ridge Cap
    piso_1.append(builder.part("roofs_ridge_cap", (183.00, 9.65, -234.00), R_ID, (0.50, 0.20, 28.20),
                               color=(35, 38, 42), material="Metal"))
    # North Gable Walls (Z = -247.45)
    piso_1.append(builder.part("roofs_gable_north_west", (180.75, 8.475, -247.45), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(105, 138, 165), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_north_east", (185.25, 8.475, -247.45), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(105, 138, 165), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    # South Gable Walls (Z = -220.45)
    piso_1.append(builder.part("roofs_gable_south_west", (180.75, 8.475, -220.45), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(105, 138, 165), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_east", (185.25, 8.475, -220.45), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(105, 138, 165), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))

    # Roof TV Antenna (on ridge at Z = -223.00)
    piso_1.append(builder.part("roofs_antenna_mast", (183.00, 12.00, -223.00), R_ID, (0.18, 5.00, 0.18),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.part("roofs_antenna_dipole_1", (183.00, 14.00, -223.00), R_ID, (2.50, 0.12, 0.12),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.part("roofs_antenna_dipole_2", (183.00, 13.00, -223.00), R_ID, (1.80, 0.12, 0.12),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.part("roofs_antenna_dipole_3", (183.00, 12.00, -223.00), R_ID, (1.20, 0.12, 0.12),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.model_close("Piso_1"))

    return "".join(piso_0), "".join(piso_1)

def build_house_33():
    # Livingroom_31_45_33 (Warm Cream with Tan Corrugated Roof)
    piso_0 = []
    
    # Skirting (Zócalo)
    piso_0.append(builder.part("skirting_west_a", (148.42, 0.35, 24.00), R_ID, (0.30, 1.70, 27.20),
                               color=(120, 122, 125), material="Concrete", textures=[("Left", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_north", (157.50, 0.35, 10.42), R_ID, (18.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete", textures=[("Back", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_east_b", (166.58, 0.35, 19.50), R_ID, (0.30, 1.70, 18.20),
                               color=(120, 122, 125), material="Concrete", textures=[("Right", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_south_b", (162.00, 0.35, 28.58), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete", textures=[("Front", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_east_a", (157.58, 0.35, 33.00), R_ID, (0.30, 1.70, 9.20),
                               color=(120, 122, 125), material="Concrete", textures=[("Right", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_south_a", (153.00, 0.35, 37.58), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete", textures=[("Front", TEX_SKIRTING, 3, 1.5)]))

    # Front Porch (North entrance door at Z=10.66, X=152.97)
    piso_0.append(builder.part("porch_deck", (152.97, 1.20, 8.50), R_ID, (5.50, 0.30, 4.00),
                               color=(130, 85, 50), material="WoodPlanks", textures=[("Top", TEX_WOOD_DECK, 2, 2)]))
    for px, pz in [(150.40, 6.65), (155.54, 6.65), (150.40, 10.35), (155.54, 10.35)]:
        piso_0.append(builder.part("porch_post", (px, 0.45, pz), R_ID, (0.25, 1.50, 0.25),
                                   color=(110, 70, 40), material="Wood"))
    piso_0.append(builder.part("porch_step_1", (152.97, 0.80, 5.90), R_ID, (3.50, 0.30, 1.20),
                               color=(130, 85, 50), material="WoodPlanks"))
    piso_0.append(builder.part("porch_step_2", (152.97, 0.40, 4.70), R_ID, (3.50, 0.30, 1.20),
                               color=(130, 85, 50), material="WoodPlanks"))
    for rx, rname in [(150.35, "west"), (155.59, "east")]:
        piso_0.append(builder.part(f"porch_rail_top_{rname}", (rx, 2.75, 8.50), R_ID, (0.18, 0.18, 4.00),
                                   color=(245, 245, 248), material="Wood"))
        piso_0.append(builder.part(f"porch_rail_bot_{rname}", (rx, 1.45, 8.50), R_ID, (0.15, 0.15, 4.00),
                                   color=(245, 245, 248), material="Wood"))
        for rz in [6.8, 7.9, 9.0, 10.1]:
            piso_0.append(builder.part(f"porch_spindle_{rname}", (rx, 2.10, rz), R_ID, (0.12, 1.20, 0.12),
                                       color=(245, 245, 248), material="Wood"))

    # Window AC Unit (on West window at X=148.67, Z=23.76, Y=4.30)
    piso_0.append(builder.part("ac_unit_casing", (147.55, 4.30, 23.76), R_ID, (1.80, 1.30, 1.80),
                               color=(215, 218, 220), material="SmoothPlastic",
                               textures=[("Left", TEX_AC_GRILL, 1.8, 1.3)]))
    piso_0.append(builder.part("ac_bracket_1", (148.00, 3.40, 23.10), R_ID, (0.80, 0.10, 0.10),
                               color=(100, 105, 110), material="Metal"))
    piso_0.append(builder.part("ac_bracket_2", (148.00, 3.40, 24.40), R_ID, (0.80, 0.10, 0.10),
                               color=(100, 105, 110), material="Metal"))

    # Porch Sconce Lamp
    piso_0.append(builder.part("porch_sconce", (155.20, 4.50, 10.50), R_ID, (0.25, 0.60, 0.25),
                               color=(30, 32, 35), material="Metal"))
    piso_0.append(builder.part("porch_light_bulb", (155.20, 4.45, 10.30), R_ID, (0.20, 0.20, 0.20),
                               color=(255, 235, 170), material="Glass",
                               point_light=(1.2, 16.0, (1.0, 0.88, 0.65))))

    # Piso_1 elements (Tan Corrugated Metal Roofs + interior ceilings)
    piso_1 = [builder.model_open("Piso_1")]
    
    # Interior flat ceilings
    piso_1.append(builder.part("roofs_interior_ceiling_a", (157.50, 7.30, 19.50), R_ID, (18.00, 0.20, 18.00),
                               color=(210, 210, 210), material="SmoothPlastic"))
    piso_1.append(builder.part("roofs_interior_ceiling_b", (153.00, 7.30, 33.00), R_ID, (9.00, 0.20, 9.00),
                               color=(210, 210, 210), material="SmoothPlastic"))

    # Section A West slope
    piso_1.append(builder.part("roofs_slope_west_a", (150.45, 8.475, 24.00), R_FALL_WEST, (28.00, 2.25, 5.10),
                               color=(145, 125, 100), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_TAN, 3, 3)]))
    # Section A East slope (rear section Z in [28.5 .. 38.0])
    piso_1.append(builder.part("roofs_slope_east_a_rear", (155.55, 8.475, 33.25), R_FALL_EAST, (9.50, 2.25, 5.10),
                               color=(145, 125, 100), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_TAN, 3, 3)]))
    # Section A Ridge Cap
    piso_1.append(builder.part("roofs_ridge_cap_a", (153.00, 9.65, 24.00), R_ID, (0.50, 0.20, 28.20),
                               color=(120, 100, 80), material="Metal"))

    # Section B East slope (Z in [10.0 .. 29.0])
    piso_1.append(builder.part("roofs_slope_east_b", (164.55, 8.475, 19.50), R_FALL_EAST, (19.00, 2.25, 5.10),
                               color=(145, 125, 100), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_TAN, 3, 3)]))
    # Section B West slope
    piso_1.append(builder.part("roofs_slope_west_b", (159.45, 8.475, 19.50), R_FALL_WEST, (19.00, 2.25, 5.10),
                               color=(145, 125, 100), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_TAN, 3, 3)]))
    # Section B Ridge Cap
    piso_1.append(builder.part("roofs_ridge_cap_b", (162.00, 9.65, 19.50), R_ID, (0.50, 0.20, 19.20),
                               color=(120, 100, 80), material="Metal"))

    # Gable walls (Warm Cream)
    piso_1.append(builder.part("roofs_gable_north_a_west", (150.75, 8.475, 10.50), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(235, 225, 205), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_north_b_east", (164.25, 8.475, 10.50), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(235, 225, 205), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_a_west", (150.75, 8.475, 37.50), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(235, 225, 205), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_a_east", (155.25, 8.475, 37.50), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(235, 225, 205), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_b_east", (164.25, 8.475, 28.50), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(235, 225, 205), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))

    # Roof TV Antenna (on Section A ridge at Z=15.00)
    piso_1.append(builder.part("roofs_antenna_mast", (153.00, 12.00, 15.00), R_ID, (0.18, 5.00, 0.18),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.part("roofs_antenna_dipole_1", (153.00, 14.00, 15.00), R_ID, (2.50, 0.12, 0.12),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.part("roofs_antenna_dipole_2", (153.00, 13.00, 15.00), R_ID, (1.80, 0.12, 0.12),
                               color=(180, 185, 190), material="Metal"))
    piso_1.append(builder.model_close("Piso_1"))

    return "".join(piso_0), "".join(piso_1)

def build_house_22():
    # Derelict_31_45_22 (Rustic White / Light Gray House)
    piso_0 = []
    
    # Skirting
    piso_0.append(builder.part("skirting_west", (106.42, 0.35, -168.00), R_ID, (0.30, 1.70, 15.20),
                               color=(120, 122, 125), material="Concrete", textures=[("Left", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_east", (115.58, 0.35, -168.00), R_ID, (0.30, 1.70, 15.20),
                               color=(120, 122, 125), material="Concrete", textures=[("Right", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_north", (111.00, 0.35, -175.58), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete", textures=[("Back", TEX_SKIRTING, 3, 1.5)]))
    piso_0.append(builder.part("skirting_south", (111.00, 0.35, -160.42), R_ID, (9.20, 1.70, 0.30),
                               color=(120, 122, 125), material="Concrete", textures=[("Front", TEX_SKIRTING, 3, 1.5)]))

    # Porch (North entrance at door Z=-175.34, X=110.97)
    piso_0.append(builder.part("porch_deck", (110.97, 1.20, -177.50), R_ID, (5.00, 0.30, 4.00),
                               color=(120, 80, 45), material="WoodPlanks", textures=[("Top", TEX_WOOD_DECK, 2, 2)]))
    piso_0.append(builder.part("porch_step_1", (110.97, 0.80, -180.10), R_ID, (3.20, 0.30, 1.20),
                               color=(120, 80, 45), material="WoodPlanks"))
    piso_0.append(builder.part("porch_step_2", (110.97, 0.40, -181.30), R_ID, (3.20, 0.30, 1.20),
                               color=(120, 80, 45), material="WoodPlanks"))
    for rx, rname in [(108.55, "west"), (113.39, "east")]:
        piso_0.append(builder.part(f"porch_rail_top_{rname}", (rx, 2.75, -177.50), R_ID, (0.18, 0.18, 4.00),
                                   color=(215, 215, 220), material="Wood"))
        piso_0.append(builder.part(f"porch_rail_bot_{rname}", (rx, 1.45, -177.50), R_ID, (0.15, 0.15, 4.00),
                                   color=(215, 215, 220), material="Wood"))
        for rz in [-179.1, -178.0, -176.9, -175.8]:
            piso_0.append(builder.part(f"porch_spindle_{rname}", (rx, 2.10, rz), R_ID, (0.12, 1.20, 0.12),
                                       color=(215, 215, 220), material="Wood"))

    # Porch Sconce Lamp
    piso_0.append(builder.part("porch_sconce", (113.20, 4.50, -175.50), R_ID, (0.25, 0.60, 0.25),
                               color=(30, 32, 35), material="Metal"))
    piso_0.append(builder.part("porch_light_bulb", (113.20, 4.45, -175.70), R_ID, (0.20, 0.20, 0.20),
                               color=(255, 235, 170), material="Glass",
                               point_light=(1.2, 16.0, (1.0, 0.88, 0.65))))

    # Piso_1 elements (Dark Corrugated Metal Gabled Roof)
    piso_1 = [builder.model_open("Piso_1")]
    piso_1.append(builder.part("roofs_slope_west", (108.45, 8.475, -168.00), R_FALL_WEST, (16.00, 2.25, 5.10),
                               color=(48, 52, 58), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_DARK, 3, 3)]))
    piso_1.append(builder.part("roofs_slope_east", (113.55, 8.475, -168.00), R_FALL_EAST, (16.00, 2.25, 5.10),
                               color=(48, 52, 58), material="Slate", cls="WedgePart",
                               textures=[("Front", TEX_ROOF_DARK, 3, 3)]))
    piso_1.append(builder.part("roofs_ridge_cap", (111.00, 9.65, -168.00), R_ID, (0.50, 0.20, 16.20),
                               color=(35, 38, 42), material="Metal"))
    # Gables
    piso_1.append(builder.part("roofs_gable_north_west", (108.75, 8.475, -175.50), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(215, 215, 220), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_north_east", (113.25, 8.475, -175.50), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(215, 215, 220), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_west", (108.75, 8.475, -160.50), R_GABLE_RISE_EAST, (0.20, 2.25, 4.50),
                               color=(215, 215, 220), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.part("roofs_gable_south_east", (113.25, 8.475, -160.50), R_GABLE_RISE_WEST, (0.20, 2.25, 4.50),
                               color=(215, 215, 220), material="SmoothPlastic", cls="WedgePart",
                               textures=[("Left", TEX_SIDING, 3, 1.5), ("Right", TEX_SIDING, 3, 1.5)]))
    piso_1.append(builder.model_close("Piso_1"))

    return "".join(piso_0), "".join(piso_1)

print("2. Generating components for all 3 houses...")
h28_p0, h28_p1 = build_house_28()
h33_p0, h33_p1 = build_house_33()
h22_p0, h22_p1 = build_house_22()

house_upgrades = {
    "Livingroom_31_45_28": (h28_p0, h28_p1),
    "Livingroom_31_45_33": (h33_p0, h33_p1),
    "Derelict_31_45_22": (h22_p0, h22_p1),
}

print("3. Streaming PZ_Rosewood.rbxlx and applying house upgrades...")

current_house = None
in_piso_0 = False
piso_0_depth = 0

# Positions of the 4 flat ceiling slabs in Suelo_Piso_1 to remove
target_positions = [
    (157.5, 7.3, 19.5),
    (153.0, 7.3, 33.0),
    (183.0, 7.3, -235.5),
    (186.0, 7.3, -222.0)
]

def is_target_slab(lines):
    text = "".join(lines)
    for tx, ty, tz in target_positions:
        # Check if coordinates are in this part
        if f"<X>{tx}</X>" in text or f"<X>{tx:.1f}</X>" in text or f"<X>{tx:.4f}</X>" in text:
            if f"<Z>{tz}</Z>" in text or f"<Z>{tz:.1f}</Z>" in text or f"<Z>{tz:.4f}</Z>" in text:
                return True
    return False

in_suelo_piso_1 = False
buffering_part = False
part_buffer = []
part_depth = 0
slabs_removed = 0

with open(BACKUP_PATH, "r", encoding="utf-8", errors="ignore") as fin, \
     open(TEMP_OUT, "w", encoding="utf-8") as fout:

    for line in fin:
        # Track Suelo_Piso_1
        if '<string name="Name">Suelo_Piso_1</string>' in line:
            in_suelo_piso_1 = True
        elif in_suelo_piso_1 and '<string name="Name">Suelo_Piso_2</string>' in line:
            in_suelo_piso_1 = False

        if in_suelo_piso_1:
            if '<Item class="Part"' in line:
                buffering_part = True
                part_depth = 1
                part_buffer = [line]
                continue
            elif buffering_part:
                part_buffer.append(line)
                if '<Item ' in line:
                    part_depth += 1
                elif '</Item>' in line:
                    part_depth -= 1
                    if part_depth == 0:
                        buffering_part = False
                        if is_target_slab(part_buffer):
                            slabs_removed += 1
                            part_buffer = []
                            continue
                        else:
                            fout.write("".join(part_buffer))
                            part_buffer = []
                            continue
                continue

        # Check for building matches
        if current_house is None:
            for hname in house_upgrades:
                if f'<string name="Name">{hname}</string>' in line:
                    current_house = hname
                    break
        elif current_house:
            if '<string name="Name">Piso_0</string>' in line:
                in_piso_0 = True
                piso_0_depth = 1

            if in_piso_0:
                if '<Item ' in line:
                    piso_0_depth += 1
                elif '</Item>' in line:
                    piso_0_depth -= 1
                    if piso_0_depth == 0:
                        # Write piso_0 components before closing Piso_0!
                        p0_xml, p1_xml = house_upgrades[current_house]
                        fout.write(p0_xml)
                        fout.write(line) # writes </Item> for Piso_0
                        # Now write piso_1 model!
                        fout.write(p1_xml)
                        in_piso_0 = False
                        current_house = None
                        continue

        fout.write(line)

print(f"  Removed {slabs_removed} redundant ceiling slabs from Suelos/Suelo_Piso_1.")
print("4. Replacing PZ_Rosewood.rbxlx with updated file...")
shutil.move(TEMP_OUT, RBXLX_PATH)
print("  Replacement complete!")
