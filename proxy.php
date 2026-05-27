<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error'=>'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input || empty($input['messages'])) {
    http_response_code(400);
    echo json_encode(['error'=>'Missing messages']);
    exit;
}

$apiKey = getenv('MINIMAX_API_KEY') ?: '';

$payload = json_encode([
    'model' => 'MiniMax-M2.7',
    'messages' => $input['messages'],
    'max_tokens' => isset($input['max_tokens']) ? $input['max_tokens'] : 1024,
    'temperature' => 0.9,
]);

$ch = curl_init('https://api.minimax.chat/v1/chat/completions');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $apiKey,
    ],
    CURLOPT_POSTFIELDS => $payload,
    CURLOPT_TIMEOUT => 30,
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200) {
    http_response_code(502);
    echo json_encode(['error'=>'Upstream error','status'=>$httpCode,'body'=>$response]);
    exit;
}

$data = json_decode($response, true);
if ($data && isset($data['choices'][0]['message']['content'])) {
    // 去掉 MiniMax M2 模型的 <think>...</think> 推理标签
    $content = $data['choices'][0]['message']['content'];
    $content = preg_replace('/<think>.*?<\/think>\s*/s', '', $content);
    $data['choices'][0]['message']['content'] = trim($content);
}

echo json_encode($data);
