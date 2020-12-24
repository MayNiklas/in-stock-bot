# in-stock-bot
[![MIT License](https://img.shields.io/github/license/MayNiklas/in-stock-bot.svg)](LICENSE)

[![GitHub Stars](https://img.shields.io/github/stars/MayNiklas/in-stock-bot.svg)](stargazers) [![GitHub Issues](https://img.shields.io/github/issues/MayNiklas/in-stock-bot.svg)](issues)

[![Lines Of Code](https://tokei.rs/b1/github/MayNiklas/in-stock-bot?category=lines)](inStockBot) [![Lines Of Code](https://tokei.rs/b1/github/MayNiklas/in-stock-bot?category=code)](inStockBot) [![Lines Of Code](https://tokei.rs/b1/github/MayNiklas/in-stock-bot?category=files)](inStockBot)

A small python Bot with Telegram notifications for checking availability of a product.

![Chat Preview](./inStockBot.jpg)

## Setup
Clone this repo to your enviroment and renama the `example-config.json` to `config.json` at first.
In the `config.json` your must add your Telegram Api Key and one or multiple products.
```json
"product": [
    {
        "name": "Produkt Name",
        "url": "https://product-url.domain/produkt/",
        "value": "This Product Is Not Available"
    },
]
```


## Usage
After you change the `config.json` File, build your Docker Container with 

```sh 
docker-compose up -d
```


## Bug / Feature Request
If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue [here](issues) by including your search query and the expected result.

If you'd like to request a new function, feel free to do so by opening an issue here. Please include sample queries and their corresponding results.

# License
| You can check out the full license [here](LICENSE).

This project is licensed under the terms of the MIT license.

[inStockBot]: <https://github.com/MayNiklas/in-stock-bot>
[stargazers]: <https://github.com/MayNiklas/in-stock-bot/stargazers>
[LICENSE]: <https://github.com/MayNiklas/in-stock-bot/LICENSE>
[issues]: <https://github.com/MayNiklas/in-stock-bot/issues>
