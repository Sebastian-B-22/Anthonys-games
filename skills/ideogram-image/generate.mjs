#!/usr/bin/env node
/**
 * Ideogram Image Generator
 * Best for: text in images, trading cards, logos
 */

import fs from 'fs';
import path from 'path';

const API_KEY = process.env.IDEOGRAM_API_KEY || '57MhOw7TC_vzswqxpd9VEDt-PYxMc8bIbgUtyvBgvVqfGoCdDYyuohS8BfktzaZyuHo_TEZicoRN2X9Yc3h8_w';

const args = process.argv.slice(2);
const getArg = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
};

const prompt = getArg('prompt');
const output = getArg('output') || './output.png';
const style = getArg('style') || 'AUTO';  // AUTO, REALISTIC, DESIGN, RENDER_3D, ANIME

if (!prompt) {
  console.error('Usage: node generate.mjs --prompt "description" [--output file.png] [--style AUTO]');
  process.exit(1);
}

async function generateImage() {
  console.log(`🎨 Ideogram generating: "${prompt.slice(0, 60)}..."`);
  
  const response = await fetch('https://api.ideogram.ai/generate', {
    method: 'POST',
    headers: {
      'Api-Key': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image_request: {
        prompt: prompt,
        model: 'V_2',
        magic_prompt_option: 'AUTO',
        style_type: style,
        aspect_ratio: 'ASPECT_1_1'
      }
    })
  });
  
  if (!response.ok) {
    const error = await response.text();
    console.error('API Error:', error);
    process.exit(1);
  }
  
  const data = await response.json();
  
  if (!data.data?.[0]?.url) {
    console.error('No image URL in response:', JSON.stringify(data, null, 2));
    process.exit(1);
  }
  
  // Download the image
  const imageUrl = data.data[0].url;
  const imageResponse = await fetch(imageUrl);
  const imageBuffer = Buffer.from(await imageResponse.arrayBuffer());
  
  const outPath = path.resolve(output);
  fs.writeFileSync(outPath, imageBuffer);
  console.log(`✅ Saved: ${outPath} (${Math.round(imageBuffer.length / 1024)}KB)`);
}

generateImage().catch(console.error);
