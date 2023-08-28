## Tracks API methods
---

> `api/v1/track/get` - get a list of tracks.

Params:
* `q` - __user request__. It may contain the _name of the artist_ or _track_.<br/>
_This param should not be used with the params_
`popular` _and_ `new`__.__
* `popular` - get tracks from __popular tracks page__.<br/>_Values: `0`, `1`.
Default: `0`._<br/>
_Should be used instead of_ `q` _param. This param should not be used with the_ `new` _param._
* `new` - get tracks from page __"New music for today"__.<br/>
_Values: `0`, `1`. Default: `0`._<br/>
_Should be used instead
of_ `q` _param. This param should not be used with the_ `popular` _param._
* `artist` _(optional)_ - option to get tracks of a specific artist from his page on the site.<br/>
_Values:_<br/>
    * `0` - tracks will be taken __from search menu.__ _With this value, the track list may contain_ ___tracks of other artists___ 
    with a similar name.<br/>
    * `1` - tracks will be taken from __artist page__ (if it exists on the site).
* `page` _(optional)_ - allows you to paginate by search results from the site. There are __48__ tracks on each page. _Default value: `1` (first page)._

__Note__: _The request must contain one of the parameters `q`, `popular`, `new`._

Request examples:

- `(your host)/api/v1/tracks/get?popular=1` - returns the 1st page from popular tracks list.
- `(your host)/api/v1/tracks/get?q=queen&artist=1&page=3` - returns the 3rd page from the list of tracks of band Queen from its page on site.
<br><br>

> `api/v1/track/download` - download a list of tracks. To find tracks, this method uses `tracks/get` method.

Params:

* `q` - search query (artist or track name).
* `mode` - download mode. There are 4 modes:
  * `all` - download all tracks from the list. This mode set by default.<br/>
  * `by_numbers` - download tracks, which numbers is equal to numbers from this param. Numbers are specified in `track_numbers` param and should be separated by commas without spaces.<br/>
  Request example: `(your host)/api/v1/tracks/download?q=queen&mode=by_numbers&track_nums=3,5,9,11`
  * `first_n` - download only first `N` tracks. Count `N` should be specified in the `n` param.<br/>
  Request example: `(your host)/api/v1/tracks/download?q=queen&mode=first_n&n=10`

  * `only_one` - download only first track.
  * `artist` - same as in `track/get` method.
  * `page` - same as in `track/get` method.
