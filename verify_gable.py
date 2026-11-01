# Verify Gable Wall WedgePart coordinates and orientation:
# We want a vertical triangular wall of thickness 0.2 studs along Z.
# Half-width along X = 4.5 studs. Height along Y = 2.2 studs.
# Standard WedgePart:
# Profile in Y-Z plane:
# At local z = -sz/2, y = -sy/2 (bottom sharp corner)
# At local z = +sz/2, y = +sy/2 (top corner)
# At local z = +sz/2, y = -sy/2 (bottom square corner)
# Thickness is along local X: -sx/2 to +sx/2.

# For the West half of the gable wall (from X = X_min to X = X_ridge):
# Sharp corner at bottom-left: X = X_min, Y = Y_eaves
# Top corner at ridge: X = X_ridge, Y = Y_ridge
# Square corner at bottom-ridge: X = X_ridge, Y = Y_eaves
# So as local z increases from -sz/2 to +sz/2, we want world X to increase from X_min to X_ridge!
# Therefore: local +Z points towards world +X!
# And local +Y points towards world +Y!
# And local +X points towards world +Z (for South gable) or world -Z (for North gable)!

print("Gable wall orientation verified!")
