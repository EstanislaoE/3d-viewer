import shutil
from pathlib import Path
import pycolmap

def run_3d_reconstruction():
    base_dir = Path(__file__).parent.resolve()
    images_dir = base_dir / "images"
    output_dir = base_dir / "output"
    
    database_path = output_dir / "database.db"
    sfm_output_dir = output_dir / "sparse"

    # CRITICAL: Remove stale database to force fresh feature extraction
    if output_dir.exists():
        print("[0/4] Cleaning up old output folder...")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    sfm_output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Feature Extraction
    print(f"[1/4] Extracting features from images in: {images_dir}")
    pycolmap.extract_features(
        database_path=database_path,
        image_path=images_dir
    )

    # 2. Feature Matching
    print("[2/4] Matching features across images...")
    pycolmap.match_exhaustive(
        database_path=database_path
    )

    # 3. Incremental Mapping (Sparse 3D Reconstruction)
    print("[3/4] Running Incremental Structure-from-Motion...")
    reconstructions = pycolmap.incremental_mapping(
        database_path=database_path,
        image_path=images_dir,
        output_path=sfm_output_dir
    )

    if not reconstructions:
        print("\n❌ Reconstruction Failed!")
        print("COLMAP could not find enough matching feature points across your images.")
        return

    model = reconstructions[0]
    
    print("\n--- Success Summary ---")
    print(f"Images successfully registered: {len(model.images)}")
    print(f"3D points generated: {len(model.points3D)}")
    
    ply_path = output_dir / "room_points.ply"
    model.export_PLY(ply_path)
    print(f" Saved 3D point cloud to: {ply_path}")

if __name__ == "__main__":
    run_3d_reconstruction()