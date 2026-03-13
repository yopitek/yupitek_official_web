// Cloudflare Worker: Contact Form API for yupitek.com
// Deploy: wrangler deploy
// Required env vars: TURNSTILE_SECRET_KEY

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': 'https://yupitek.com',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    let data;
    try {
      data = await request.json();
    } catch {
      return Response.json({ error: 'Invalid JSON' }, { status: 400 });
    }

    // Input validation
    const { name, email, subject, message } = data;
    if (!name || !email || !subject || !message) {
      return Response.json({ error: 'Missing required fields' }, { status: 400 });
    }
    if (name.length > 100 || email.length > 200 || subject.length > 200 || message.length > 5000) {
      return Response.json({ error: 'Input too long' }, { status: 400 });
    }

    // Validate Cloudflare Turnstile CAPTCHA
    const turnstileToken = data['cf-turnstile-response'];
    if (!turnstileToken) {
      return Response.json({ error: 'CAPTCHA required' }, { status: 400 });
    }

    const verifyParams = new URLSearchParams({
      secret: env.TURNSTILE_SECRET_KEY,
      response: turnstileToken,
      remoteip: request.headers.get('CF-Connecting-IP') || '',
    });

    const turnstileRes = await fetch(
      'https://challenges.cloudflare.com/turnstile/v0/siteverify',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: verifyParams.toString(),
      }
    );
    const turnstileData = await turnstileRes.json();
    if (!turnstileData.success) {
      return Response.json({ error: 'CAPTCHA verification failed' }, { status: 400 });
    }

    // Sanitize: strip HTML tags from user inputs
    const sanitize = (str) => str.replace(/<[^>]*>/g, '').trim();
    const safeName = sanitize(name);
    const safeEmail = sanitize(email);
    const safeSubject = sanitize(subject);
    const safeMessage = sanitize(message);

    // Send email via MailChannels
    const emailBody = [
      '新訊息來自 yupitek.com 官網聯絡表單',
      '',
      `姓名: ${safeName}`,
      `Email: ${safeEmail}`,
      `主旨: ${safeSubject}`,
      `訊息:`,
      safeMessage,
      '',
      '---',
      `IP: ${request.headers.get('CF-Connecting-IP') || 'unknown'}`,
      `時間: ${new Date().toISOString()}`,
    ].join('\n');

    const mailRes = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [{
          to: [{ email: 'eason@yupitek.com', name: 'Eason Lai' }],
          reply_to: { email: safeEmail, name: safeName },
        }],
        from: { email: 'noreply@yupitek.com', name: 'Yopitek Website' },
        subject: `[yupitek.com] ${safeSubject} — ${safeName}`,
        content: [{ type: 'text/plain', value: emailBody }],
      }),
    });

    if (!mailRes.ok) {
      return Response.json({ error: 'Email delivery failed' }, { status: 502 });
    }

    return Response.json({ success: true }, {
      headers: { 'Access-Control-Allow-Origin': 'https://yupitek.com' }
    });
  },
};
