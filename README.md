# ivapi
Simple implementation of Telegram Instant View pages generator

# Instant View template example
https://instantview.telegram.org
```
?path: ^/iv/.+\.html(\?.+)?

body:     //article
title:    $body//h1[1]
description: $body//p[normalize-space()]
description: $title

image_url:   $cover/self::img/@src
```
