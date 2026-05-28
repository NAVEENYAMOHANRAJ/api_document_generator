<?php

use Illuminate\Support\Facades\Route;

Route::get('/laravel-users', 'UserController@index');
Route::post('/laravel-users', 'UserController@store');
Route::delete('/laravel-users/{id}', 'UserController@destroy');
