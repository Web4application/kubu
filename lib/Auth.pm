package Auth;
use strict;
use warnings;
use Crypt::Bcrypt qw(bcrypt);
use Digest::SHA qw(sha256_hex);
use DB qw(get_user_by_username insert_user update_password);
use Exporter 'import';

our @EXPORT_OK = qw(authenticate_user generate_session_token);

sub validate_password_policy {
    my ($password) = @_;

    die "Password must be at least 12 characters long." if length($password) < 12;
    die "Password must contain uppercase, lowercase, digit, and special character."
        unless $password =~ /[A-Z]/ && $password =~ /[a-z]/ && $password =~ /\d/ && $password =~ /[\W_]/;

    return 1;
}

sub authenticate_user {
    my ($username, $password) = @_;
    my $user = get_user_by_username($username);

    return unless $user;
    return bcrypt($password, $user->{password}) eq $user->{password};
}

sub generate_session_token {
    my $user = shift;
    return sha256_hex($user . time);
}

1;
