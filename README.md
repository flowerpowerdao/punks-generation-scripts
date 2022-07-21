# Instructions 🛠

## preparation 🍱

-   create folder in root of project called `assets`
-   add your assets to the `assets` folder
-   cd into `generator`
-   run `poetry install`
-   adapt the `generator.py`, `oracle.py` and `utils.py` files to your needs
-   change `generator = 'ethflower_generator.generator:stop_mint'` to `generator = 'ethflower_generator.generator:assemble_svgs'`
-   make sure you use the right constants at the top of `generator.py`
-   run `poetry run generator`
-   profit? 💫

## helpers 💪

### decrease size of pngs in batch

```bash
for name in *.png
do
    sips -Z 200 "$name" -o "_thumbnail_${name}"
done
```

### rename in batch

```bash
 for name in *                                                                                                                        ✔
do
    mv "$name" "_thumbnail_${name}"
done
```

### remove prefix in batch

```bash
for file in *;do
mv $file ${file#BG_}
done
```

### swap prefix and suffix in batch

```bash
for file in WHITE_*;do                                                        ✔
name=${file#WHITE_}
echo mv $file ${name%.png}_WHITE.png
done
```

## uploading 💾

-   you cant upload the entire collection at once, split it in half and upload each half
