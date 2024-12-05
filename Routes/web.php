<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\SettingsController;

Route::get('/', function () {
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

<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class HomeController extends Controller
{
public function index()
{
return view('home');
}
}
use App\Http\Controllers\HomeController;

Route::get('/home', [HomeController::class, 'index']);
