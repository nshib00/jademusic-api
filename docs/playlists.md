## Playlist API methods


> `api/v1/playlist/get` - get a list of popular playlists.

Params:
* `page` _(optional)_ - allows you to paginate by search results from the site. There are __52__ playlists on each page. _Default value: `1` (first page)._<br>_If page number is greater than count of playlist pages on the site, the last page will be returned._


Request example:<br>
`(your host)/api/v1/playlist/get` - returns 1st page from playlists list.
`(your host)/api/v1/playlist/get?page=3` - returns 3rd page.


> `api/v1/playlist/download` - download a playlist. To find playlists, this method uses `playlist/get` method.

Params:
* `playlist_id` ___(required)___ - download a playlist with specific number in the list.
* `page` _(optional)_ - same as in `playlist/get`.

Request example:
`(your host)/api/v1/playlist/download?album_id=14` - download 14th album from 1st page from the site.

