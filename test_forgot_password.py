#!/usr/bin/env python3
"""
Test script for forgot password functionality
"""

import requests
import json

API = 'http://localhost:8000/api/auth'

print('=' * 60)
print('FORGOT PASSWORD FEATURE - COMPLETE FLOW TEST')
print('=' * 60)
print()

# Test 1: Register a new user
print('📝 Test 1: Register a new user')
print('-' * 60)
try:
    response = requests.post(f'{API}/register', json={
        'username': 'testuser123',
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'✅ User registered: {data["user"]["username"]}')
    else:
        print(f'Response: {response.text}')
except Exception as e:
    print(f'❌ Error: {e}')
print()

# Test 2: Request password reset
print('🔐 Test 2: Request password reset')
print('-' * 60)
try:
    response = requests.post(f'{API}/forgot-password', json={
        'email': 'test@example.com'
    })
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        reset_code = data.get('reset_code')
        print(f'✅ Password reset requested')
        print(f'Reset Code: {reset_code}')
    else:
        print(f'Response: {response.text}')
        reset_code = None
except Exception as e:
    print(f'❌ Error: {e}')
    reset_code = None
print()

if reset_code:
    # Test 3: Reset password with the code
    print('🔄 Test 3: Reset password with code')
    print('-' * 60)
    try:
        response = requests.post(f'{API}/reset-password', json={
            'email': 'test@example.com',
            'reset_code': reset_code,
            'new_password': 'NewPass456'
        })
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Password reset successful!')
            print(f'Message: {data["message"]}')
        else:
            print(f'Response: {response.text}')
    except Exception as e:
        print(f'❌ Error: {e}')
    print()

    # Test 4: Try to login with new password
    print('🚀 Test 4: Login with new password')
    print('-' * 60)
    try:
        response = requests.post(f'{API}/login', json={
            'username': 'testuser123',
            'password': 'NewPass456'
        })
        print(f'Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'✅ SUCCESS! User logged in with new password')
            print(f'User: {data["user"]["username"]}')
            print(f'Token Type: {data["token_type"]}')
        else:
            print(f'❌ Failed: {response.text}')
    except Exception as e:
        print(f'❌ Error: {e}')
else:
    print('⚠️  Skipping reset tests because reset code was not obtained')

print()
print('=' * 60)
print('TEST COMPLETE')
print('=' * 60)
