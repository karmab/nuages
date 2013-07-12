            var host = null, port = null;
            var sc;

            function spice_set_cookie(name, value, days) {
                var date, expires;
                date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toGMTString();
                document.cookie = name + "=" + value + expires + "; path=/";
            };

            function spice_query_var(name, defvalue) {
                var match = RegExp('[?&]' + name + '=([^&]*)')
                                  .exec(window.location.search);
                return match ?
                    decodeURIComponent(match[1].replace(/\+/g, ' '))
                    : defvalue;
            }

            function spice_error(e)
            {
                disconnect();
            }

            function connect()
            {
                var host, port, password, scheme = "ws://", uri;

                // By default, use the host and port of server that served this file
                host = '{{ information.host }}';
                port = '{{ information.port }}';

                // If a token variable is passed in, set the parameter in a cookie.
                // This is used by nova-spiceproxy.
                token = spice_query_var('token', null);
                if (token) {
                    spice_set_cookie('token', token, 1)
                }

                password = '{{ information.ticket }}';
                path = spice_query_var('path', 'websockify');

                if ((!host) || (!port)) {
                    console.log("must specify host and port in URL");
                    return;
                }

                if (sc) {
                    sc.stop();
                }

                uri = scheme + host + ":" + port;

                try
                {
                    sc = new SpiceMainConn({uri: uri, screen_id: "spice-screen", dump_id: "debug-div",
                                message_id: "message-div", password: password, onerror: spice_error });
                }
                catch (e)
                {
                    alert(e.toString());
                    disconnect();
                }

            }

            function disconnect()
            {
                console.log(">> disconnect");
                if (sc) {
                    sc.stop();
                }
                console.log("<< disconnect");
            }

            connect();
