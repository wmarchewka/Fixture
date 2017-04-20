#!/usr/bin/perl

require '.\unit_upload.pl';

$unit_ip = shift;
$user = shift;
$password = shift;
$slot = shift;
$file = shift;
upload_unit($unit_ip,$user,$password,$slot,$file);

