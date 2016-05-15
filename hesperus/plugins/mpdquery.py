from ..plugin import CommandPlugin

import mpd

class MPDQuery(CommandPlugin):
    @CommandPlugin.config_types(mpdhost=str, mpdport=int, replyprefix=str, replypostfix=str, notplayingstr=str)
    def __init__(self, core, mpdhost, replyprefix, replypostfix, notplayingstr, mpdport=6600):
        super(MPDQuery, self).__init__(core)

        self.mpdhost = mpdhost
        self.mpdport = mpdport
        self.replyprefix = replyprefix
        self.replypostfix = replypostfix
        self.notplaying = notplayingstr

    @CommandPlugin.register_command("music")
    def music(self, chans, name, match, direct, reply):
        client = mpd.MPDClient()
        client.connect(self.mpdhost, self.mpdport)
        status = client.status()
        songinfo = client.currentsong()
        client.disconnect()

        if status['state'] == "play":
            title = songinfo.get('title', '')
            artist = songinfo.get('artist', '')
            album = songinfo.get('album', '')
            name = songinfo.get('name', '')

            if title and artist and album:
                reply("%s %s - %s - %s. %s" % (
                self.replyprefix,
                title,
                artist,
                album,
                self.replypostfix,
                ))
            elif title and artist:
                reply("%s %s by %s. %s" % (
                    self.replyprefix,
                    title,
                    artist,
                    self.replypostfix,
                    ))
            elif title:
                reply("%s %s. %s" % (
                    self.replyprefix,
                    title,
                    self.replypostfix,
                    ))
            elif name:
                reply("%s \"%s\" %s" % (
                    self.replyprefix,
                    name,
                    self.replypostfix,
                    ))
            else:
                reply("%s <unknown> %s" % (
                    self.replyprefix,
                    self.replypostfix,
                    ))
        else:
            reply(self.notplaying)
