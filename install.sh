#!/bin/bash

echo "🚀 INICIANDO INSTALAÇÃO DO CYBERPIXEL..."

# 1. Instalar Dependências
echo "📦 Instalando bibliotecas Python..."
pip3 install pygame pillow pyinstaller

# 2. Criar Executável
echo "🔨 Compilando binário (Isso pode demorar um pouco no Pi)..."
pyinstaller --noconsole --onefile --name="CyberPixel" CyberPixel.py

# 3. Criar Pastas e Mover Arquivos
echo "📂 Organizando arquivos..."
mkdir -p $HOME/Apps/CyberPixel
cp dist/CyberPixel $HOME/Apps/CyberPixel/
cp CyberPixelLogo.png $HOME/Apps/CyberPixel/

# 4. Criar Atalho no Menu
echo "📝 Criando atalho no Menu..."
cat > $HOME/.local/share/applications/cyberpixel.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=CyberPixel
Comment=Editor de Pixel Art 8-bit
Exec=$HOME/Apps/CyberPixel/CyberPixel
Icon=$HOME/Apps/CyberPixel/CyberPixelLogo.png
Terminal=false
Categories=Graphics;2DGraphics;
StartupWMClass=CyberPixelApp
EOL

# 5. Permissão de Execução
chmod +x $HOME/.local/share/applications/cyberpixel.desktop

echo "✅ SUCESSO! CyberPixel instalado. Procure no seu Menu Iniciar."
