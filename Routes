Route::get('/welcome', function () {
return view('welcome');
});

Route::get('/home', [HomeController::class, 'index']);

Route::get('/user/{id}', function ($id) {
return 'User '.$id;
});

Route::get('/profile', [ProfileController::class, 'show'])->name('profile');

Route::middleware(['auth'])->group(function () {
Route::get('/dashboard', [DashboardController::class, 'index']);
Route::get('/settings', [SettingsController::class, 'index']);
});
