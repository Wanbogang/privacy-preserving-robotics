# Privacy-Preserving Home Robotics Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18090716.svg)](https://doi.org/10.5281/zenodo.18090716)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Robots yang membantu tanpa mengawasi. Functionality without surveillance.**

## 🎯 Apa Ini?

Framework untuk robot rumah yang menyelesaikan paradoks privacy-functionality melalui 4 pilar:

1. **Identity without Identification** - Mengenali kontinuitas tanpa biometrik
2. **Memory without Recording** - Mengingat pola tanpa log kejadian
3. **Learning without Raw Data** - Belajar dari feedback tanpa dataset observasi
4. **Explainability without Privacy Breach** - Menjelaskan keputusan tanpa ungkap data surveillance

## 📄 Paper

Baca paper lengkap: [paper/main.md](paper/main.md)

**DOI**: [10.5281/zenodo.18090716](https://doi.org/10.5281/zenodo.18090716)

## 🏗️ Arsitektur
```
Sensor (Non-ID) → Feature Extraction → Ephemeral Identity 
→ Pattern Memory → Context Understanding → Action & Explanation
```

## 🚀 Quick Start
```bash
git clone https://github.com/Wanbogang/privacy-preserving-robotics.git
cd privacy-preserving-robotics
pip install -r requirements.txt
```

## 📚 Dokumentasi

- [Arsitektur Detail](docs/ARCHITECTURE.md)
- [Use Cases](docs/USE_CASES.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🎯 Use Cases

- **Eldercare** - Deteksi jatuh tanpa kamera
- **Disability Assistance** - Bantuan proaktif dengan dignitas
- **Multi-Person Home** - Asisten kontekstual tanpa surveillance keluarga

## 🤝 Berkontribusi

Kontribusi terbuka! Lihat [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License

GPL-3.0 - Software bebas yang melindungi kebebasan pengguna

## 📖 Citation
```bibtex
@software{setiawan2024privacy,
  author = {Setiawan, Agus},
  title = {Privacy-Preserving Home Robotics Framework},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.18090716}
}
```

## 👤 Author

**Agus Setiawan**  
📧 harapan.bontang@gmail.com  
📍 Wonosobo, Central Java, Indonesia

## 🙏 Acknowledgments

This work is independent research conducted during the author's engagement with the open source robotics community.

---

*Privacy bukan constraint yang diminimalkan, tapi prinsip desain yang membuat robot lebih trustworthy.*
