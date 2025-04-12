package KubuHai::Authen::Digest_MD5;

use strict;
use warnings;
use base qw(KubuHai::Authen::Perl);  # Inherit from the base class
use Digest::MD5 qw(md5_hex);

# Method to start the client authentication
sub client_start {
    my ($self) = @_;
    return '';  # No initial string, just an empty string to start the process
}

# Method for client step (response to challenge)
sub client_step {
    my ($self, $challenge) = @_;
    my ($user, $pass) = map {
        my $v = $self->{callback}->{$_};
        defined($v) ? $v : ''
    } qw(user pass);

    # Digest-MD5 step: MD5 hash of the concatenation of password and challenge
    return $user . " " . md5_hex($pass . $challenge);
}

1;
