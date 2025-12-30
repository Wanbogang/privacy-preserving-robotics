# Privacy-Preserving Home Robotics Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18090716.svg)](https://doi.org/10.5281/zenodo.18090716)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Helpful robots without surveillance. Functionality without compromising privacy.**

## 🎯 Overview

A framework for home robotics that resolves the privacy-functionality paradox through four architectural pillars. This approach enables robots to understand human context and provide meaningful assistance while eliminating personal data storage, biometric identification, and surveillance mechanisms.

### Four Pillars

1. **Identity without Identification** - Recognize behavioral continuity without biometric data
2. **Memory without Recording** - Remember patterns without logging events
3. **Learning without Raw Data** - Adapt through feedback without observation datasets
4. **Explainability without Privacy Breach** - Explain decisions without revealing surveillance data

## 📄 Paper

Read the complete framework: [paper/main.md](paper/main.md)

**Published**: [DOI: 10.5281/zenodo.18090716](https://doi.org/10.5281/zenodo.18090716)

**Title**: "Privacy-Preserving Human Understanding for Home Robotics: A Framework for Continuity Without Surveillance"

## 🏗️ Architecture

```
Sensor (Non-ID) → Feature Extraction → Ephemeral Identity 
→ Pattern Memory → Context Understanding → Action & Explanation
```

The framework consists of six layers that work together to provide robot functionality without surveillance:

1. **Sensor Layer** - Non-identifiable sensors (LiDAR, depth, thermal, pressure)
2. **Feature Extraction** - Immediate abstraction, raw data discarded
3. **Ephemeral Identity** - Behavioral continuity without biometric ID
4. **Pattern Memory** - Abstract patterns, no event logs
5. **Context Understanding** - Anomaly detection, situation assessment
6. **Action & Explanation** - Execute behaviors, provide transparent reasoning

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Wanbogang/privacy-preserving-robotics.git
cd privacy-preserving-robotics

# Install dependencies
pip install -r requirements.txt

# Run example
python examples/fall_detection_demo.py
```

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - Detailed system design with algorithms
- [Use Cases](docs/USE_CASES.md) - Five real-world scenarios with privacy analysis
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to the project

## 🎯 Use Cases

### 1. Eldercare Fall Detection
Monitor elderly persons for safety without camera surveillance. Detect falls and unusual patterns while preserving dignity.

### 2. Disability Assistance
Provide proactive assistance for mobility-impaired individuals without creating surveillance records or health data logs.

### 3. Multi-Person Households
Contextual assistance for families without facial recognition or enabling parental surveillance of children.

### 4. Sleep Monitoring
Track sleep patterns to detect health issues without bedroom cameras or invasive monitoring.

### 5. Medication Reminders
Provide medication prompts and detect concerning non-response patterns without logging compliance data.

See [docs/USE_CASES.md](docs/USE_CASES.md) for detailed scenarios.

## 🔬 Key Features

### Privacy by Design
- No biometric data storage
- No event logging with timestamps
- No reconstructable personal information
- Ephemeral identities only
- Pattern-based memory, not events
- Learning without raw data retention

### Functional Capabilities
- Behavioral continuity across sessions
- Anomaly detection and health monitoring
- Contextual assistance and proactive support
- Pattern-based explanations
- Adaptive learning from user feedback

## 🤝 Contributing

Contributions are welcome! We're looking for:

- [ ] Core algorithm implementations
- [ ] Sensor integration examples
- [ ] Privacy-preserving learning methods
- [ ] Documentation and tutorials
- [ ] Use case demonstrations
- [ ] Testing and benchmarks

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Privacy Review Checklist

All contributions must maintain privacy-preserving properties:

- [ ] No biometric data storage
- [ ] No event logging with timestamps
- [ ] No reconstructable personal information
- [ ] Ephemeral identities only
- [ ] Pattern-based memory, not events
- [ ] Learning without raw data storage
- [ ] Explanations don't reveal surveillance data

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

**Why GPL-3.0?**
- Ensures software freedom
- Protects against proprietary capture
- Requires sharing improvements
- Preserves open development model

## 📖 Citation

If you use this framework in your research, please cite:

```bibtex
@software{setiawan2024privacy,
  author       = {Setiawan, Agus},
  title        = {Privacy-Preserving Home Robotics Framework},
  year         = {2024},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18090716},
  url          = {https://doi.org/10.5281/zenodo.18090716}
}
```

## 🌟 Project Status

**Current Phase**: Framework design and documentation complete

**Next Steps**:
- Reference implementation of core algorithms
- Sensor integration examples
- Simulation environment
- Real-world deployment testing

## 👤 Author

**Agus Setiawan**  
Independent Researcher  
📧 harapan.bontang@gmail.com  
📍 Bojonegoro, East Java, Indonesia

## 🙏 Acknowledgments

This work is independent research conducted during the author's engagement with the open source robotics community. Special thanks to OpenMind project contributors for valuable discussions and inspiration.

## 💡 Philosophy

> Privacy is not a constraint to be minimized, but a design principle that makes robots more trustworthy.

This framework demonstrates that robots can be helpful without being invasive. We believe technology should enhance human dignity, not diminish it.

## 📞 Contact

**Questions or collaborations?**
- Email: harapan.bontang@gmail.com
- GitHub Issues: [Report issues or suggest features](https://github.com/Wanbogang/privacy-preserving-robotics/issues)
- Discussions: [Join the conversation](https://github.com/Wanbogang/privacy-preserving-robotics/discussions)

## 🔗 Links

- **Paper (Zenodo)**: https://doi.org/10.5281/zenodo.18090716
- **Repository**: https://github.com/Wanbogang/privacy-preserving-robotics
- **Documentation**: [docs/](docs/)

---

**Built with the belief that privacy and functionality are not mutually exclusive.**
