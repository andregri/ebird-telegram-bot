# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0](https://github.com/andregri/ebird-telegram-bot/compare/v1.0.0...v1.1.0) (2023-06-17)


### Features

* create a set of common names from search result ([0d08cc8](https://github.com/andregri/ebird-telegram-bot/commit/0d08cc85e1b12070fdb195edc3b904bb453c1488))
* download photos ([a1a9d86](https://github.com/andregri/ebird-telegram-bot/commit/a1a9d863cdee3aa29689ec13fee4ee3c64d0e543))
* quiz poll to identify bird from image ([990575e](https://github.com/andregri/ebird-telegram-bot/commit/990575e909de984df0ffe4af768766250cdcbbab))
* send a custom message to all users once the bot restarts ([7afd31c](https://github.com/andregri/ebird-telegram-bot/commit/7afd31c7b9a8410f71b3285d7e92ead8ac66a69f))

## 1.0.0 (2023-06-03)


### Features

* add license ([4833263](https://github.com/andregri/ebird-telegram-bot/commit/4833263ecb58a59575cadf47a86bb9052b20e8fa))
* add semantic release pipeline ([a5b2ed7](https://github.com/andregri/ebird-telegram-bot/commit/a5b2ed7dac84dc0c0bbe890a85562cdf85d760bd))
* async upload of db backup ([478602a](https://github.com/andregri/ebird-telegram-bot/commit/478602a8b80b8018b6c5c50effb5c4f2f6365194))
* backup and restore db to and from free.keep.sh ([489412c](https://github.com/andregri/ebird-telegram-bot/commit/489412c3c8eb902ec6d1fc73d86c0a86edce5069))
* command to list following ([1471edc](https://github.com/andregri/ebird-telegram-bot/commit/1471edc41c3305602aa9617ddc81020928092015))
* create Database class to store connection ([bfeb890](https://github.com/andregri/ebird-telegram-bot/commit/bfeb890d2ff76dd029074234a960b422c25dc896))
* create sqlite db ([1ff2624](https://github.com/andregri/ebird-telegram-bot/commit/1ff26246f47e6c23427edbe129ea5311f3f6119b))
* disable info logs from httpx ([328b59b](https://github.com/andregri/ebird-telegram-bot/commit/328b59b56d0294d2c2ea37074be69abcbc9f04a1))
* enable bot logging ([674cc40](https://github.com/andregri/ebird-telegram-bot/commit/674cc40d49c36d892c978473499a99e13923083e))
* fetch all rows from db ([a995791](https://github.com/andregri/ebird-telegram-bot/commit/a995791cd1000b6287d966bde0e7b2da8e3d9c7b))
* function to check if already following ([e012522](https://github.com/andregri/ebird-telegram-bot/commit/e0125220a29b779e6325837593f747624dd057df))
* insert and delete follower ([78aa168](https://github.com/andregri/ebird-telegram-bot/commit/78aa16822df84b2b5ec0f7298de647591616edc3))
* jobs table foreign key references the followers table pk ([f8198de](https://github.com/andregri/ebird-telegram-bot/commit/f8198de2045b0b4e378ccd54ea8d5f18427aaf90))
* list followings from db ([99f1b42](https://github.com/andregri/ebird-telegram-bot/commit/99f1b426f036eb7291d618af9061b8d337ce4ae2))
* log number of bytes uploaded ([4c95317](https://github.com/andregri/ebird-telegram-bot/commit/4c95317d5b80be30ac24f5908b51e639025e5915))
* logging in list_following ([bca42bf](https://github.com/andregri/ebird-telegram-bot/commit/bca42bfdf781fbfc93fde9e25a0ddfcd85e48a21))
* remove dict for caching followings ([0dbc2dd](https://github.com/andregri/ebird-telegram-bot/commit/0dbc2dd868287f1c37f0d78c3aff5b212b62b261))
* remove jobs table ([dcdf02c](https://github.com/andregri/ebird-telegram-bot/commit/dcdf02c2dd295bbf5491d045ea795f92e2f55f43))
* schedule all jobs when bot starts ([dc7f1ac](https://github.com/andregri/ebird-telegram-bot/commit/dc7f1ac4cd4a6fa8743be8d8f16d6b1380f450ea))
* unfollow removes from db ([cd79930](https://github.com/andregri/ebird-telegram-bot/commit/cd7993049f21f15cecdae70874755597c432f378))


### Bug Fixes

* disable web page preview for db messages ([f262e14](https://github.com/andregri/ebird-telegram-bot/commit/f262e14efc802e18fc666d7e2c3564fc598d1d8b))
* disable web page preview for db messages ([063fe2b](https://github.com/andregri/ebird-telegram-bot/commit/063fe2bcd92bda9f55aaeb73a8b49a4683308574))
* log only info ([0ebbcb6](https://github.com/andregri/ebird-telegram-bot/commit/0ebbcb6f03dec7fc16be89af5feb20513f293794))
* no need to set log config ([4201bf5](https://github.com/andregri/ebird-telegram-bot/commit/4201bf5cbfa442c49aaf4dc1706c75463d32a7d1))
* typo in table name ([b7c9a94](https://github.com/andregri/ebird-telegram-bot/commit/b7c9a944346bc0b15b142c1c0744b7b3651d1e8e))
