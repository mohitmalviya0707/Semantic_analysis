import zipfile
import json
import shutil
import os

INPUT_MODEL = "Artifacts/BiGRU_Model.keras"
BACKUP_MODEL = "Artifacts/BiGRU_Model_backup.keras"
OUTPUT_MODEL = "Artifacts/BiGRU_Model_fixed.keras"


# ---------------------------------------------------------
# 1. Create backup
# ---------------------------------------------------------

if not os.path.exists(BACKUP_MODEL):
    shutil.copy2(INPUT_MODEL, BACKUP_MODEL)
    print("Backup created:", BACKUP_MODEL)
else:
    print("Backup already exists.")


# ---------------------------------------------------------
# 2. Read the .keras file
# ---------------------------------------------------------

with zipfile.ZipFile(INPUT_MODEL, "r") as zin:

    print("\nFiles inside model:")
    for name in zin.namelist():
        print(" -", name)

    # Read model configuration
    model_config = json.loads(
        zin.read("config.json").decode("utf-8")
    )


# ---------------------------------------------------------
# 3. Remove unsupported quantization_config
# ---------------------------------------------------------

removed_count = 0


def remove_quantization_config(obj):

    global removed_count

    if isinstance(obj, dict):

        if "quantization_config" in obj:

            del obj["quantization_config"]

            removed_count += 1

        for value in obj.values():

            remove_quantization_config(value)

    elif isinstance(obj, list):

        for item in obj:

            remove_quantization_config(item)


remove_quantization_config(model_config)

print(
    f"\nRemoved quantization_config from {removed_count} locations."
)


# ---------------------------------------------------------
# 4. Create repaired .keras model
# ---------------------------------------------------------

with zipfile.ZipFile(INPUT_MODEL, "r") as zin:

    with zipfile.ZipFile(
        OUTPUT_MODEL,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zout:

        for item in zin.infolist():

            # Replace config.json with repaired version
            if item.filename == "config.json":

                repaired_config = json.dumps(
                    model_config,
                    ensure_ascii=False
                ).encode("utf-8")

                zout.writestr(
                    item,
                    repaired_config
                )

            else:

                zout.writestr(
                    item,
                    zin.read(item.filename)
                )


print("\nFixed model created successfully:")
print(OUTPUT_MODEL)

print("\nNow test the repaired model.")