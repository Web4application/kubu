#!/usr/bin/perl

use strict;
use warnings;
use lib 'lib';
use Auth qw(authenticate_user generate_session_token);
use DB qw(create_tables insert_user);
use MFA qw(generate_otp send_otp verify_otp);

# Initialize DB and create tables
create_tables();

# Registration (for testing purposes)
print "Register new user (username): ";
my $username = <STDIN>;
chomp($username);

print "Enter password: ";
my $password = <STDIN>;
chomp($password);

# Password Policy Validation
eval { Auth::validate_password_policy($password) };
if ($@) {
    print "Password policy error: $@\n";
    exit;
}

# Insert user
my $hashed_password = bcrypt($password, 12);
insert_user($username, $hashed_password);

# Authentication
print "\nLogin - Enter username: ";
my $login_username = <STDIN>;
chomp($login_username);

print "Enter password: ";
my $login_password = <STDIN>;
chomp($login_password);

if (authenticate_user($login_username, $login_password)) {
    print "Password verified. Sending OTP...\n";
    my $otp = generate_otp();
    send_otp('user@example.com', $otp);

    print "Enter OTP: ";
    my $input_otp = <STDIN>;
    chomp($input_otp);

    if (verify_otp($login_username, $input_otp)) {
        my $session_token = generate_session_token($login_username);
        print "Authentication successful. Session Token: $session_token\n";
    } else {
        print "Invalid OTP.\n";
    }
} else {
    print "Invalid username or password.\n";
}
