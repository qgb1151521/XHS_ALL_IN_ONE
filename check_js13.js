const fs = require('fs');
const code = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');

eval(code);

try {
    const result = get_request_headers_params('/api/test', '', 'test_a1_cookie');
    console.log('Function call success!');
    console.log('Result:', result);
} catch (e) {
    console.log('Function call error:', e.message);
    console.log('Stack:', e.stack);
}