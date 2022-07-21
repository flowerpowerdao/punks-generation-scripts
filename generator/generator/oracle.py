def add_oracle(soup):
    """adds a price oracle to the template"""

    # add a new script tag to the svg
    new_script = soup.new_tag("script")

    # append the oracle logic to it
    new_script.append("""
    fetch(
    "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true"
)
    .then((response) => response.json())
    .then((priceChange) => {
        let usd24HourChange = priceChange.ethereum.usd_24h_change.toFixed(2);
        updateAnimationDuration(usd24HourChange);
    })
    .catch((err) => console.log(err));

function updateAnimationDuration(usd24HourChange) {
    let styleSheets = document.styleSheets;
    for (let i = 2; i < 22; i++) {
        let animationDuration = parseFloat(
            styleSheets[0].cssRules[i].style.animationDuration
        );
        let updatedDuration = calculateAnimationDuration(
            usd24HourChange,
            animationDuration
        );
        let updatedDurationString = updatedDuration.toString() + "s";
        styleSheets[0].cssRules[i].style.animationDuration =
            updatedDurationString;
    }
}

function calculateAnimationDuration(usd24HourChange, initialValue) {
    let g = initialValue * 2;
    let k = 1 / (50 * initialValue);
    let newValue =
        g *
        (
            1 /
            (1 + Math.exp(k * g * usd24HourChange) * (g / initialValue - 1))
        ).toFixed(3);
    return newValue === 0 ? 0.001 : newValue;
}

""")
    soup.svg.append(new_script)
