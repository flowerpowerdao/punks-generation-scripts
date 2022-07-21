from bs4 import BeautifulSoup
from pathlib import Path
from generator.utils import pick_choice
from generator.utils import calculate_weights, check_for_triples, get_filenames, add_assets, add_petal_animation, get_trait, print_progress_bar
from generator.oracle import add_oracle
from generator.plot import plot_bar
import generator.weights as weights
import json
import csv


ASSET_CANISTER_URL = "https://zt63f-rqaaa-aaaae-qadaq-cai.raw.ic0.app/"
# ASSET_CANISTER_URL = "./"
COLLECTION_NAME = "punks"
COLLECTION_SIZE = 7761 # + 16 uniques = 7777


def assemble_svgs():
    """assemble the svgs for the collection"""

    # get all the relative filenames for the different layers.
    # specify substrings in exclude_list to exclude certain files by substrings
    backgrounds = get_filenames("../assets/BACKGROUNDS",
                                exclude_list=["thumbnail", ".DS_Store"])
    background_accessories = get_filenames(
        "../assets/BACKGROUND_ACCESSORIES", exclude_list=["thumbnail", ".DS_Store"])

    body_heads = get_filenames(
        "../assets/BODY_HEAD", exclude_list=["thumbnail", ".DS_Store"])

    top_head_leafs = get_filenames(
        "../assets/BODY_HEAD_BASIC/TOP_HEAD_LEAFS", exclude_list=["thumbnail", ".DS_Store"])

    top_head_crowns = get_filenames(
        "../assets/BODY_HEAD_BASIC/TOP_HEAD_CROWNS", exclude_list=["thumbnail", ".DS_Store"])

    top_head_chains = get_filenames(
        "../assets/BODY_HEAD_BASIC/TOP_HEAD_CHAINS", exclude_list=["thumbnail", ".DS_Store"])

    masks = get_filenames(
        "../assets/MASKS", exclude_list=["thumbnail", ".DS_Store"])

    eyes = get_filenames(
        "../assets/MID_HEAD/EYES", exclude_list=["thumbnail", ".DS_Store"])

    accessories = get_filenames(
        "../assets/MID_HEAD/ACCESSORIES", exclude_list=["thumbnail", ".DS_Store"])

    bottom_head_accessories = get_filenames(
        "../assets/MID_HEAD/BOTTOM_HEAD_ACCESSORIES", exclude_list=["thumbnail", ".DS_Store"])

    body_accessories = get_filenames(
        "../assets/BODY_ACCESSORIES/BODY", exclude_list=["thumbnail", ".DS_Store"])

    necks = get_filenames(
        "../assets/BODY_ACCESSORIES/NECK", exclude_list=["thumbnail", ".DS_Store"])

    frames = get_filenames(
        "../assets/FRONT_FRAME", exclude_list=["thumbnail", ".DS_Store"])

    lasers = get_filenames(
        "../assets/LASER_EYE", exclude_list=["thumbnail", ".DS_Store"])

    uniques = get_filenames(
        "../assets/UNIQUES", exclude_list=["thumbnail", ".DS_Store"])

    # get the path to the template svg file the assets will be embedded in
    template = Path(__file__).parent / "template.svg"

    # open the template file and get the soup
    # this has to be done twice because we have call by reference
    with template.open() as svg_template:
        soup = BeautifulSoup(svg_template, 'xml')

    with template.open() as svg_template:
        lowres_soup = BeautifulSoup(svg_template, 'xml')
    # the oracle code has to be added to the template only once
    # add_oracle(soup)
    # add_oracle(lowres_soup)

    nfts = []

    for i in range(COLLECTION_SIZE):

        print_progress_bar(i, COLLECTION_SIZE, "Progress", "Complete")

        background, lowres_background = pick_choice(
            backgrounds, weights.background)

        background_accessory, lowres_background_accessory = pick_choice(
            background_accessories, weights.background_accessory)

        body_head, lowres_body_head = pick_choice(
            body_heads, weights.body_head)

        top_head_leaf, lowres_top_head_leaf = pick_choice(
            top_head_leafs, weights.top_head_leaf)
        top_head_crown, lowres_top_head_crown = pick_choice(
            top_head_crowns, weights.top_head_crown)
        top_head_chain, lowres_top_head_chain = pick_choice(
            top_head_chains, weights.top_head_chain)
        mask, lowres_mask = pick_choice(masks, weights.mask)

        # those are only present when the punk doesnt wear a mask
        eye, lowres_eye = pick_choice(eyes, weights.eye)
        accessory, lowres_accessory = pick_choice(
            accessories, weights.accessory)
        bottom_head_accessory, lowres_bottom_head_accessory = pick_choice(
            bottom_head_accessories, weights.bottom_head_accessory)

        body_accessory, lowres_body_accessory = pick_choice(
            body_accessories, weights.body_accessory)
        neck, lowres_neck = pick_choice(
            necks, weights.neck)
        frame, lowres_frame = pick_choice(
            frames, weights.frame)

        laser, lowres_laser = pick_choice(
            lasers, weights.laser)

        # check if mask is present and we use it instead
        if not 'NONE' in mask:
            eye, lowres_eye = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'
            accessory, lowres_accessory = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'
            bottom_head_accessory, lowres_bottom_head_accessory = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'

        # check if bodyhead string contains btcflowerbrain
        if 'BTCFLOWERBRAIN' in body_head:
            top_head_leaf, lowres_top_head_leaf = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'
            top_head_crown, lowres_top_head_crown = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'
            top_head_chain, lowres_top_head_chain = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'

        # headphones dont work with btcflower brain
        if 'BTCFLOWERBRAIN' in body_head and 'HEADPHONES' in accessory:
            accessory, lowres_accessory = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'

        # neck accessories dont work with hoodies or jackets
        if 'WINTER' in body_accessory or 'HOODIE' in body_accessory:
            neck, lowres_neck = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'

        # googles and glasses dont work with laser eyes and other accessories
        if 'GOGGLES' in eye or 'GLASSES' in eye:
            laser, lowres_laser = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'
            accessory, lowres_accessory = 'BODY_HEAD_BASIC/NONE.png', 'BODY_HEAD_BASIC/_thumbnail_NONE.png'

        add_assets(
            soup,
            ASSET_CANISTER_URL,
            background=background,
            background_accessory=background_accessory,
            body_head=body_head,
            top_head_leaf=top_head_leaf,
            top_head_crown=top_head_crown,
            top_head_chain=top_head_chain,
            mask=mask,
            eye=eye,
            accessory=accessory,
            bottom_head_accessory=bottom_head_accessory,
            body_accessory=body_accessory,
            neck=neck,
            frame=frame,
            laser=laser,
        )

        add_assets(
            lowres_soup,
            ASSET_CANISTER_URL,
            background=lowres_background,
            background_accessory=lowres_background_accessory,
            body_head=lowres_body_head,
            top_head_leaf=lowres_top_head_leaf,
            top_head_crown=lowres_top_head_crown,
            top_head_chain=lowres_top_head_chain,
            mask=lowres_mask,
            eye=lowres_eye,
            accessory=lowres_accessory,
            bottom_head_accessory=lowres_bottom_head_accessory,
            body_accessory=lowres_body_accessory,
            neck=lowres_neck,
            frame=lowres_frame,
            laser=lowres_laser,
        )

        with Path("../assets/"+str(i+1)+".svg").open('w') as random_svg:
            random_svg.write(str(soup))
        with Path("../assets/"+str(i+1)+"_thumbnail.svg").open('w') as random_svg_low:
            random_svg_low.write(str(lowres_soup))

        nfts.append(
            {
                "mint_number": i+1,
                "background": get_trait(background),
                "background_accessory": get_trait(background_accessory),
                "body_head": get_trait(body_head),
                "top_head_leaf": get_trait(top_head_leaf),
                "top_head_crown": get_trait(top_head_crown),
                "top_head_chain": get_trait(top_head_chain),
                "mask": get_trait(mask),
                "eye": get_trait(eye),
                "accessory": get_trait(accessory),
                "bottom_head_accessory": get_trait(bottom_head_accessory),
                "body_accessory": get_trait(body_accessory),
                "neck": get_trait(neck),
                "frame": get_trait(frame),
                "laser": get_trait(laser),
                'unique': 'NONE'
            }
        )

    # build uniques
    for id, item in enumerate(uniques):
        unique, lowres_unique = pick_choice([item], [1])
        add_assets(
            soup,
            ASSET_CANISTER_URL,
            unique=unique,
        )

        add_assets(
            lowres_soup,
            ASSET_CANISTER_URL,
            unique=lowres_unique,
        )

        with Path("../assets/"+str(7761+id+1)+".svg").open('w') as random_svg:
            random_svg.write(str(soup))
        with Path("../assets/"+str(7761+id+1)+"_thumbnail.svg").open('w') as random_svg_low:
            random_svg_low.write(str(lowres_soup))

        nfts.append(
            {
                "mint_number": 7761+id+1,
                "background": 'NONE',
                "background_accessory": 'NONE',
                "body_head": 'NONE',
                "top_head_leaf": 'NONE',
                "top_head_crown": 'NONE',
                "top_head_chain": 'NONE',
                "mask": 'NONE',
                "eye": 'NONE',
                "accessory": 'NONE',
                "bottom_head_accessory": 'NONE',
                "body_accessory": 'NONE',
                "neck": 'NONE',
                "frame": 'NONE',
                "laser": 'NONE',
                'unique': get_trait(unique, ".jpg"),
            }
        )

    with open(f'{COLLECTION_NAME}.json', 'w') as f:
        json.dump(nfts, f, ensure_ascii=False, indent=4)

    with open(f'{COLLECTION_NAME}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(
            ["mint_number", "background", "background_accessory", "body_head", "top_head_leaf", "top_head_crown", "top_head_chain", "mask", "eye", "accessory", "bottom_head_accessory", "body_accessory", "neck", "frame", "laser"])
        for entry in nfts:
            spamwriter.writerow(
                [entry["mint_number"], entry["background"], entry["background_accessory"], entry["body_head"], entry["top_head_leaf"], entry["top_head_crown"], entry["top_head_chain"], entry["mask"], entry["eye"], entry["accessory"], entry["bottom_head_accessory"], entry["body_accessory"], entry["neck"], entry["frame"], entry["laser"]])


def stop_mint():
    print("you already minted")
