# 🏗️ Project Restructure Plan: app → backend

## 🎯 Target Structure
```
jp/                                  # Project root
├── backend/                         # Backend code (was app/)
│   ├── api/                         # FastAPI routes
│   ├── data/                        # Database models & repositories  
│   ├── services/                    # Business logic services
│   ├── utils/                       # Utility functions
│   ├── __init__.py                  # Package initialization
│   ├── config.py                    # Configuration
│   ├── logger.py                    # Logging setup
│   └── requirements.txt             # Backend runtime dependencies
├── tests/                           # All tests (keep at root)
├── frontend/                        # Frontend code (future)
├── requirements-ci.txt              # CI/Dev tools (root level)
├── pyproject.toml                   # Root config (updated paths)
└── .github/workflows/              # CI/CD (updated paths)
```

## 📋 Migration Checklist

### Phase 1: Dependency Split & Structure Prep
- [ ] **1.1** Split `requirements.txt` into runtime vs CI dependencies
- [ ] **1.2** Create `backend/requirements.txt` with runtime deps only
- [ ] **1.3** Update root `requirements-ci.txt` with dev/CI tools only
- [ ] **1.4** Create new directory structure

### Phase 2: Code Movement
- [ ] **2.1** Move `app/` → `backend/` (wholesale directory move)
- [ ] **2.2** Verify all files moved correctly
- [ ] **2.3** Update directory references (if any)

### Phase 3: Python Import Updates
- [ ] **3.1** Update all Python imports: `from app.` → `from backend.`
- [ ] **3.2** Update all Python imports: `import app.` → `import backend.`
- [ ] **3.3** Update internal cross-references within backend code

### Phase 4: Configuration Updates  
- [ ] **4.1** Update `pyproject.toml` - known-first-party: `["app"]` → `["backend"]`
- [ ] **4.2** Update `pyproject.toml` - testpaths: `["tests"]` (no change needed)
- [ ] **4.3** Update `.pre-commit-config.yaml` - file patterns to scan `backend/`

### Phase 5: CI/CD Pipeline Updates
- [ ] **5.1** Update GitHub Actions - dependency installation paths
- [ ] **5.2** Update GitHub Actions - syntax validation paths  
- [ ] **5.3** Update GitHub Actions - test execution paths
- [ ] **5.4** Update GitHub Actions - code quality check paths

### Phase 6: Verification & Testing
- [ ] **6.1** Test local development environment
- [ ] **6.2** Test pre-commit hooks
- [ ] **6.3** Test CI pipeline (if possible)
- [ ] **6.4** Verify import resolution
- [ ] **6.5** Clean up temporary files

## 🔍 Files That Need Import Updates

Based on analysis, these **21 Python files** contain `app.` imports:

### Backend Code Files (will be moved to backend/)
1. `app/api/old/applications.py` - 3 references
2. `app/api/old/applications_simple.py` - 18 references  
3. `app/api/old/enhanced_jobs_api.py` - 1 reference
4. `app/api/old/resume_api.py` - 10 references
5. `app/api/old/skill_bank.py` - 4 references
6. `app/api/old/timeline.py` - 3 references
7. `app/api/old/user_profiles.py` - 3 references
8. `app/config.py` - 1 reference
9. `app/data/company_repository.py` - 3 references
10. `app/data/database.py` - 8 references
11. `app/data/interaction_repository.py` - 6 references
12. `app/data/mock_data_generator.py` - 12 references
13. `app/data/resume_repository.py` - 4 references
14. `app/data/skill_bank_repository.py` - 3 references
15. `app/logger.py` - 1 reference
16. `app/services/llm_service.py` - 1 reference
17. `app/services/pdf_generation_service.py` - 2 references
18. `app/services/resume_generation_service.py` - 4 references
19. `app/services/resume_orchestrator_service.py` - 7 references
20. `app/services/timeline_service.py` - 1 reference
21. `app/utils/retry.py` - 1 reference

### Configuration Files (stay at root)
- `pyproject.toml` - Update `known-first-party = ["backend"]`
- `.github/workflows/test-suite.yml` - Update paths and import tests

## 🔄 Import Pattern Changes

### Current Patterns → New Patterns
```python
# Pattern 1: Direct module imports
from app.data.models import UserProfile
from app.config import settings
→
from backend.data.models import UserProfile  
from backend.config import settings

# Pattern 2: Submodule imports
import app.data.database
import app.logger
→
import backend.data.database
import backend.logger

# Pattern 3: Complex imports
from app.data.models import Base, UserProfileDB, JobListingDB
→
from backend.data.models import Base, UserProfileDB, JobListingDB
```

## 🛡️ Risk Mitigation

### Low Risk Changes
- ✅ **Directory move**: Safe, just file system operation
- ✅ **Dependency split**: Clear separation, well-defined
- ✅ **Configuration updates**: Clear, isolated changes

### Medium Risk Changes  
- ⚠️ **Import updates**: Many files, but systematic find/replace
- ⚠️ **CI pipeline updates**: Multiple workflow files to update

### Safety Measures
1. **Backup approach**: Git provides full rollback capability
2. **Systematic approach**: Update imports in logical order
3. **Incremental testing**: Test after each phase
4. **Pattern consistency**: Use consistent find/replace patterns

## 🔧 Implementation Strategy

### Automated Find/Replace Patterns
```bash
# Safe systematic replacement (will be scripted)
find backend/ -name "*.py" -type f -exec sed -i 's/from app\./from backend\./g' {} \;
find backend/ -name "*.py" -type f -exec sed -i 's/import app\./import backend\./g' {} \;
```

### Order of Operations
1. **Preparation** - Create new structure, split dependencies
2. **Move** - Wholesale directory move (preserves git history)  
3. **Update** - Systematic import updates
4. **Configure** - Update config files
5. **Test** - Verify everything works
6. **Deploy** - Update CI/CD

## ⚡ Execution Time Estimate
- **Preparation**: 15 minutes
- **Directory move**: 2 minutes  
- **Import updates**: 10 minutes (scripted)
- **Configuration**: 10 minutes
- **Testing**: 15 minutes
- **Total**: ~50 minutes

## 🎉 Post-Migration Benefits
- ✅ **Clear separation** - Backend vs frontend vs tests
- ✅ **Intuitive structure** - `backend/` clearly identifies Python code  
- ✅ **Dependency clarity** - Runtime deps separate from dev tools
- ✅ **Future-ready** - Easy to add frontend alongside
- ✅ **Maintainable** - Logical, industry-standard organization

---

**Ready to execute this plan?** The approach is systematic and low-risk with full git rollback capability.
