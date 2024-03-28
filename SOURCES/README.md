# ea-tomcat101 EA4 container based package

## Security

Please read https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html
to find ways to increase security of your tomcat instance.

## Faster Startup

Please read https://go.cpanel.net/TomcatFastStart
to find ways to improve the startup time for your tomcat instance.

## Test Script

`/opt/cpanel/ea-tomcat101/test.jsp` is a handy JSP test script that you can copy to try out your instance.

See _How do I deploy my code?_ to learn about deployment.

## How do I deploy my code?

There are various ways to deploy your code, each with its own security implications. The method that you use will depend on your needs, circumstances, and risk tolerance. **Because of that, and because we are not tomcat experts, cPanel does not provide specific direction on how to configure tomcat or tomcat applications.** Our default configuration is designed to allow you to make informed choices and pick the best method for your use case.

To determine which method is the best for you, read [Tomcat’s Security](https://tomcat.apache.org/tomcat-10.1-doc/security-howto.html) documentation. Then, read the [Tomcat Web Application Deployment](https://tomcat.apache.org/tomcat-10.1-doc/deployer-howto.html) documentation to choose the method you wish to use.

## How do I start/stop/etc my container?

It is managed by the `ea-podman` system.

* https://docs.cpanel.net/ea4/containers/the-ea-podman-script/
  * via CLI `/usr/local/cpanel/scripts/ea-podman hint` to get started
* https://docs.cpanel.net/ea4/containers/tomcat-via-containers/

## How do I find my tomcat container’s AJP and HTTP ports?

1. Run `/usr/local/cpanel/scripts/ea-podman list`
2. Find the entry for your instance name
3. The `ports` field is a list of ports.
4. The first is for HTTP protocols
5. The second is for the AJP protocol

## I want to access my apps via URI and not need a port number

You simply need to configure your web server to proxy a given URI to the appropriate port.

For example:

* given an AJP port of `11111`
* assuming you want `example.com/testuri` to serve the test.jsp noted above

You’d need to:

1. create a `ProxyPass` include for Apache.
   * An [include for `example.com`](https://docs.cpanel.net/ea4/apache/modify-apache-virtual-hosts-with-include-files/) would look like this:
```
<IfModule proxy_ajp_module>
    ProxyPass "/testuri" "ajp://127.0.0.1:11111/test.jsp"
</IfModule>
```
2. restart apache
3. Hit example.com/testuri to ensure it took effect

**Note**: The ajp module in that example is brought in as a requirement of `ea-tomcat101`.

## I want to access my HTTP port via SSL

For example:

* given an HTTP port of `11110`
* you want to do `https://your-domain.example:11110` instead of the default `http://your-domain.example:11110`

You’d need to:

1. Change the container’s `conf/server.xml` HTTP connector (`<Connector port="8080" protocol="HTTP/1.1" …` to be SSL per [tomcat’s SSL how to](https://tomcat.apache.org/tomcat-10.1-doc/ssl-howto.html).
   * **Note**: We **strongly** advise against storing passwords in a plaintext.
   * Any files that need accessed inside the container:
      1. should exist in `~/ea-podman.d/ea-tomcat101.…/` directory
      2. can be referenced by using paths relative to the instance’s `~/ea-podman.d/ea-tomcat101.…/` directory
2. Restart your container
3. Now `https://your-domain.example:11110` should work and `http://your-domain.example:11110` should not.
