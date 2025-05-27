use Test::More;
use lib 'lib';
use Auth qw(authenticate_user);
use DB qw(insert_user);
use Crypt::Bcrypt qw(bcrypt);

# Setup test user
my $test_username = 'testuser';
my $test_password = 'Secure123!';
my $hashed_password = bcrypt($test_password, 12);
insert_user($test_username, $hashed_password);

ok(authenticate_user($test_username, $test_password), "User authenticated successfully");

done_testing();
