## Albums API methods

> `api/v1/tracks/get` - get a list of popular albums.

__Note:__ _if there are any singles, track collections or playlists in the album list, they are also counted as albums._

Params:
* `page` _(optional)_ - allows you to paginate by search results from the site. There are __40__ albums on each page. _Default value: `1` (first page)._<br>_If page number is greater than count of album pages on the site, the last page will be returned._


Request example:<br>
`(your host)/api/v1/album/get` - returns 1st page from popular albums list.
`(your host)/api/v1/album/get?page=5` - returns 5th page.


> `api/v1/album/download` - download an album from list of albums. To find albums, this method uses `album/get` method.

Params:
* `album_id` ___(required)___ - download an album with specific number in the list.
* `page` _(optional)_ - same as in `album/get`.

Request example:
`(your host)/api/v1/album/download?page=2&album_id=7` - download 7th album from 2nd page from the site.

