from pathlib import Path
import trimesh

ply_path = Path("output/room_points.ply")

if ply_path.exists():
    # Load sparse point cloud
    pcd = trimesh.load(str(ply_path))
    points = pcd.vertices
    colors = pcd.colors if hasattr(pcd, 'colors') and pcd.colors is not None else [255, 0, 0, 255]

    print(f"Loaded point cloud with {len(points)} points.")

    scene = trimesh.Scene()

    # Convert single pixel points into small visible 3D spheres
    for point in points:
        sphere = trimesh.creation.icosphere(subdivisions=1, radius=0.03)
        sphere.apply_translation(point)
        scene.add_geometry(sphere)

    # Mouse Controls in Pop-Up Window:
    # - Left Click + Drag  : Rotate Scene
    # - Right Click + Drag : Pan Scene
    # - Mouse Wheel        : Zoom In / Out
    scene.show()
else:
    print("File output/room_points.ply not found!")