#!/bin/bash
set -e  # Isso faz o script parar IMEDIATAMENTE se der erro (vital para debug)

echo "🚀 CORRIGINDO INSTALAÇÃO DO CYBERPIXEL (MODO BOOKWORM)..."

# 1. Instalar Dependências via APT (O jeito nativo do Raspberry Pi)
# Isso é muito mais rápido que compilar via pip
echo "📦 Instalando bibliotecas do sistema..."
sudo apt update
sudo apt install -y python3-pygame python3-pil python3-pip

# 2. Instalar PyInstaller (Com a flag mágica para o Bookworm)
echo "📦 Instalando PyInstaller..."
# A flag --break-system-packages é necessária no OS novo para instalar apps de usuário
pip3 install pyinstaller --break-system-packages

# Garante que o terminal enxergue o comando pyinstaller
export PATH=$PATH:$HOME/.local/bin

# 3. Criar Executável
echo "🔨 Compilando binário (Isso demora uns 2 minutos no Pi, aguarde)..."
# Limpa tentativas anteriores
rm -rf build dist
# --clean ajuda a evitar cache corrompido
pyinstaller --noconsole --onefile --clean --name="CyberPixel" CyberPixel.py

# Verifica se o arquivo foi criado mesmo
if [ ! -f "dist/CyberPixel" ]; then
    echo "❌ ERRO CRÍTICO: O arquivo 'dist/CyberPixel' não foi criado!"
    exit 1
fi

# 4. Criar Pastas e Mover Arquivos
echo "📂 Organizando arquivos..."
mkdir -p $HOME/Apps/CyberPixel
cp dist/CyberPixel $HOME/Apps/CyberPixel/
cp CyberPixelLogo.png $HOME/Apps/CyberPixel/

# 5. Criar Atalho no Menu
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

# 6. Permissão de Execução
chmod +x $HOME/.local/share/applications/cyberpixel.desktop
chmod +x $HOME/Apps/CyberPixel/CyberPixel

echo "✅ SUCESSO TOTAL! Pode abrir o CyberPixel no menu."
