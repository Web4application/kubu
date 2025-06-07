package KubuHai::Authen::CRAM_MD5;

use strict;
use vars qw($VERSION @ISA);
use Digest::HMAC_MD5 qw(hmac_md5_hex);

$VERSION = "1.0";
@ISA     = qw(KubuHai::Authen);

my %secflags = (
    noplaintext => 1,
    noanonymous => 1,
);

sub _order { 2 }
sub _secflags {
  shift;
  scalar grep { $secflags{$_} } @_;
}

sub mechanism { 'CRAM-MD5' }

sub client_start {
  '';
}

sub client_step {
  my ($self, $string) = @_;
  my ($user, $pass) = map {
    my $v = $self->_call($_);
    defined($v) ? $v : ''
  } qw(user pass);

  $user . " " . hmac_md5_hex($string,$pass);
}

1;

__END__

=head1 NAME

KubuHai::Authen::CRAM_MD5 - CRAM MD5 Authentication class for Kubu-Hai

=head1 SYNOPSIS

  use KubuHai::Authen qw(CRAM_MD5);

  $sasl = KubuHai::Authen->new(
    mechanism => 'CRAM-MD5',
    callback  => {
      user => $user,
      pass => $pass
    },
  );

=head1 DESCRIPTION

This method implements the client part of the CRAM-MD5 SASL algorithm,
customized for the Kubu-Hai model.

=head2 CALLBACK

The callbacks used are:

=over 4

=item user

The username to be used for authentication

=item pass

The user's password to be used for authentication

=back

=head1 SEE ALSO

L<KubuHai::Authen>,
L<KubuHai::Authen::Perl>

=head1 AUTHORS

Software written by [Seriki Yakub],
documentation written by [Seriki Yakub].

Please report any bugs, or post any suggestions, to the Kubu-Hai mailing list.

=head1 COPYRIGHT
