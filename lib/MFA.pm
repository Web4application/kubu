package MFA;
use strict;
use warnings;
use Email::Sender::Simple qw(sendmail);
use Email::Simple;
use Email::Simple::Creator;
use Config::Simple;
use Exporter 'import';

our @EXPORT_OK = qw(generate_otp send_otp verify_otp);

my $cfg = Config::Simple->new('config.cfg');
my %otp_store;

sub generate_otp {
    my $otp = int(rand(1000000));
    return sprintf("%06d", $otp);
}

sub send_otp {
    my ($email, $otp) = @_;

    my $email_obj = Email::Simple->create(
        header => [
            To      => $email,
            From    => $cfg->param('otp_sender_email'),
            Subject => "Your OTP Code",
        ],
        body => "Your OTP code is: $otp",
    );

    sendmail($email_obj);
}

sub verify_otp {
    my ($user, $input_otp) = @_;
    return $otp_store{$user} && $otp_store{$user} eq $input_otp;
}

1;
