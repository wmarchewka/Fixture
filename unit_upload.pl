#!/usr/bin/perl
#tcpclient.pl

use IO::Socket::INET;
use File::Copy;
use File::Glob qw(bsd_glob);
use File::Spec;
use File::Basename;
use Getopt::Std;
use Net::SMTP;
use MIME::Base64;


sub upload_unit
{
   my($unit_ip) = $_[0];
   my($user) = $_[1];
   my($password) = $_[2];
   my($slot) = $_[3];
   my($file) = $_[4];

   my $socket;
   my $authorization = encode_base64($user.":".$password,"");

   print "Uploading $file to $unit_ip\n";
   # creating object interface of IO::Socket::INET modules which internally creates
   # socket, binds and connects to the TCP server running on the specific port.
   $socket = new IO::Socket::INET( PeerHost => $unit_ip, PeerPort => '80', Proto => 'tcp',) or die "ERROR in Socket Creation \n";

   ## Create the body of the request. This countains:
   #  - the delimiter
   #  - the form data (name specifies  where the image is to be loaded, one of 
   #        - web for web pages
   #        - certs for SSL certificate
   #        - meter for meter chip firmware
   #        - wifi for wifi chip firmware
   #        - image for the Starline firmware image
   # - content type and 
   # - the image to load
   my $req_body = "-----------------------------7dd3201c5104d4\r\n".
   "Content-Disposition: form-data; name=\"".$slot."\"; filename=\"".$file."\"\r\n".
   "Content-Type: application/octet-stream\r\n".
   "\r\n";

   open FILE, $file;
   binmode FILE;
   while (<FILE>) {
       $req_body .= $_;
   }
   close FILE;

   $req_body = $req_body . "\r\n-----------------------------7dd3201c5104d4\r\n";

   # Now create the request header. This has to be done after the body since the 
   # header contains the length of the body
   # Note that the request also contains the authorization in base64 encoding.
   # The cuurent encoded authorization is for the factory login. This needs to be changed
   # to encode a user supplied name and passowrd. 
   my $req_head = "POST /upload_file.cgi HTTP/1.1\r\n" .
   "Accept-Language: en-us\r\n".
   "Host: 192.168.1.100\r\n".
   "Content-Type: multipart/form-data; boundary=---------------------------7dd3201c5104d4\r\n".
   "Content-Length: ". length($req_body) ."\r\n".
   "Connection: Keep-Alive\r\n".
   "Authorization: Basic ".$authorization."\r\n\r\n".
   "\r\n";

   # Send the request
   $socket->send($req_head . $req_body);

   # Get the response
   my $response = "";
   while ($data = <$socket>) {
      $response .= $data; 
      #print $data;
   }   

   # Done with the socket, so close it
   $socket->close();

   # Check to see if the upload was successful
   if ($response =~ /upload\.html/) {
      print $file. " uploaded to " .$slot ."\n";
   } else {
      print "Failed to upload ". $file ."\n";
   }
}

1; # need to end with a true value

