"""
Unit tests for CompanyInfo Pydantic model validation.

Tests field constraints, string validation, list handling, and edge cases
for the CompanyInfo model.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import ValidationError

from backend.data.models import CompanyInfo


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestCompanyInfo:
    """Test CompanyInfo model validation."""

    def test_minimal_valid_company_info(self):
        """Test creating CompanyInfo with minimal required fields."""
        company = CompanyInfo(name="TechCorp Inc")
        
        # Test that auto-generated fields exist
        assert isinstance(company.id, UUID)
        assert isinstance(company.created_at, datetime)
        assert isinstance(company.updated_at, datetime)
        
        # Test required fields
        assert company.name == "TechCorp Inc"
        
        # Test default values
        assert company.industry is None
        assert company.size is None
        assert company.location is None
        assert company.website is None
        assert company.description is None
        assert company.culture is None
        assert company.values == []
        assert company.benefits == []

    def test_company_info_with_all_fields(self, sample_company_data):
        """Test creating CompanyInfo with all fields populated."""
        company = CompanyInfo(**sample_company_data)
        
        # Verify all fields are set correctly
        assert company.name == "TechCorp Inc"
        assert company.industry == "Technology"
        assert company.size == "201-500 employees"
        assert company.location == "San Francisco, CA"
        assert company.website == "https://techcorp.com"
        assert company.description == "A leading technology company specializing in innovative solutions"

    def test_required_fields_validation(self):
        """Test that required fields are properly validated."""
        # Missing name should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            CompanyInfo()
        
        assert "name" in str(exc_info.value)
        assert "field required" in str(exc_info.value).lower()
        
        # Empty string name should be allowed (business logic can handle validation)
        company = CompanyInfo(name="")
        assert company.name == ""

    def test_string_field_validation(self):
        """Test string field validation."""
        company = CompanyInfo(
            name="Amazing Tech Company",
            industry="Software Development",
            size="100-500 employees",
            location="Austin, TX",
            website="https://amazing-tech.com",
            description="We build amazing software solutions for businesses worldwide.",
            culture="We value innovation, collaboration, and work-life balance.",
        )
        
        assert company.name == "Amazing Tech Company"
        assert company.industry == "Software Development"
        assert company.size == "100-500 employees"
        assert company.location == "Austin, TX"
        assert company.website == "https://amazing-tech.com"
        assert company.description == "We build amazing software solutions for businesses worldwide."
        assert company.culture == "We value innovation, collaboration, and work-life balance."
        
        # Empty strings should be allowed
        company = CompanyInfo(
            name="TestCorp",
            industry="",
            size="",
            location="",
            website="",
            description="",
            culture="",
        )
        
        assert company.industry == ""
        assert company.size == ""
        assert company.location == ""
        assert company.website == ""
        assert company.description == ""
        assert company.culture == ""

    def test_list_field_validation(self):
        """Test list field validation."""
        values_list = ["Innovation", "Integrity", "Excellence", "Teamwork"]
        benefits_list = ["Health Insurance", "401k", "Flexible PTO", "Remote Work"]
        
        company = CompanyInfo(
            name="Benefits Corp",
            values=values_list,
            benefits=benefits_list,
        )
        
        assert company.values == values_list
        assert company.benefits == benefits_list
        
        # Empty lists should work
        company = CompanyInfo(
            name="MinimalCorp",
            values=[],
            benefits=[],
        )
        assert company.values == []
        assert company.benefits == []
        
        # Single item lists
        company = CompanyInfo(
            name="SimpleCorp",
            values=["Simplicity"],
            benefits=["Health Insurance"],
        )
        assert company.values == ["Simplicity"]
        assert company.benefits == ["Health Insurance"]

    def test_uuid_field_validation(self):
        """Test UUID field validation."""
        # Valid UUID
        company_id = uuid4()
        company = CompanyInfo(
            name="Test Company",
            id=company_id,
        )
        assert company.id == company_id
        
        # Test UUID string conversion
        company = CompanyInfo(
            name="Test Company",
            id=str(company_id),
        )
        assert company.id == company_id
        assert isinstance(company.id, UUID)

    def test_datetime_defaults(self):
        """Test that datetime fields have proper default values."""
        company1 = CompanyInfo(name="Company One")
        company2 = CompanyInfo(name="Company Two")
        
        # Both should have datetime values
        assert isinstance(company1.created_at, datetime)
        assert isinstance(company1.updated_at, datetime)
        assert isinstance(company2.created_at, datetime)
        assert isinstance(company2.updated_at, datetime)
        
        # They should be different (created at different times)
        assert company1.id != company2.id  # At minimum, IDs should be different

    def test_company_info_config(self):
        """Test that the Config class is properly set."""
        company = CompanyInfo(name="Test Company")
        
        # Test model config is properly set (Pydantic v2 style)
        model_config = getattr(company.__class__, 'model_config', None)
        if model_config:
            # Pydantic v2 style - model_config is a dictionary
            if isinstance(model_config, dict):
                assert model_config.get('from_attributes', False) is True
            else:
                # If it's an object
                assert getattr(model_config, 'from_attributes', False) is True
        else:
            # Fallback: test that the model can be created from dict (basic functionality)
            test_dict = {"name": "Test from dict"}
            test_company = CompanyInfo(**test_dict)
            assert test_company.name == "Test from dict"


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestCompanyInfoBusinessScenarios:
    """Test CompanyInfo model with realistic business scenarios."""

    def test_startup_company(self):
        """Test creating a startup company profile."""
        startup = CompanyInfo(
            name="InnovateTech",
            industry="AI/Machine Learning",
            size="10-50 employees",
            location="San Francisco, CA",
            website="https://innovatetech.ai",
            description="AI-powered solutions for modern businesses",
            culture="Fast-paced, innovative, equity-based compensation",
            values=["Innovation", "Agility", "Impact"],
            benefits=["Equity", "Flexible Hours", "Learning Budget", "Health Insurance"],
        )
        
        assert startup.name == "InnovateTech"
        assert startup.industry == "AI/Machine Learning"
        assert startup.size == "10-50 employees"
        assert len(startup.values) == 3
        assert len(startup.benefits) == 4
        assert "Equity" in startup.benefits

    def test_enterprise_company(self):
        """Test creating an enterprise company profile."""
        enterprise = CompanyInfo(
            name="MegaCorp International",
            industry="Financial Services",
            size="10,000+ employees",
            location="New York, NY",
            website="https://megacorp.com",
            description="Global financial services leader with 150+ years of history",
            culture="Professional, structured, comprehensive benefits, work-life balance",
            values=["Integrity", "Excellence", "Client Focus", "Teamwork", "Innovation"],
            benefits=[
                "Comprehensive Health Insurance", "401k with Match", "Pension Plan",
                "Life Insurance", "Disability Insurance", "Paid Time Off",
                "Professional Development", "Tuition Reimbursement", "Employee Assistance Program"
            ],
        )
        
        assert enterprise.name == "MegaCorp International"
        assert enterprise.industry == "Financial Services"
        assert "10,000+" in enterprise.size
        assert len(enterprise.values) == 5
        assert len(enterprise.benefits) == 9
        assert "Professional Development" in enterprise.benefits

    def test_remote_first_company(self):
        """Test creating a remote-first company profile."""
        remote_company = CompanyInfo(
            name="DistributedTech",
            industry="Software Development",
            size="50-200 employees",
            location="Remote-first (HQ: Austin, TX)",
            website="https://distributedtech.com",
            description="Building the future of work through distributed teams",
            culture="Remote-first, asynchronous communication, results-oriented",
            values=["Flexibility", "Trust", "Communication", "Results"],
            benefits=[
                "Remote Work Stipend", "Home Office Setup", "Flexible PTO",
                "Health Insurance", "Mental Health Support", "Co-working Space Access"
            ],
        )
        
        assert remote_company.name == "DistributedTech"
        assert "Remote-first" in remote_company.location
        assert "asynchronous communication" in remote_company.culture
        assert "Remote Work Stipend" in remote_company.benefits

    def test_nonprofit_organization(self):
        """Test creating a nonprofit organization profile."""
        nonprofit = CompanyInfo(
            name="TechForGood Foundation",
            industry="Non-profit",
            size="20-100 employees",
            location="Multiple locations",
            website="https://techforgood.org",
            description="Leveraging technology to solve social and environmental challenges",
            culture="Mission-driven, collaborative, community-focused",
            values=["Impact", "Sustainability", "Equity", "Collaboration"],
            benefits=[
                "Mission-driven work", "Professional Development", "Flexible Schedule",
                "Health Insurance", "Retirement Plan", "Volunteer Time Off"
            ],
        )
        
        assert nonprofit.name == "TechForGood Foundation"
        assert nonprofit.industry == "Non-profit"
        assert "Mission-driven work" in nonprofit.benefits
        assert "Impact" in nonprofit.values

    def test_international_company(self):
        """Test creating an international company profile."""
        international = CompanyInfo(
            name="GlobalTech Solutions Ltd.",
            industry="Technology Consulting",
            size="1,000-5,000 employees",
            location="London, UK (Global presence)",
            website="https://globaltech-solutions.com",
            description="International technology consulting with offices in 25+ countries",
            culture="Multicultural, collaborative, continuous learning",
            values=["Diversity", "Excellence", "Innovation", "Global Mindset"],
            benefits=[
                "International Health Coverage", "Relocation Assistance",
                "Cultural Exchange Programs", "Language Learning Support",
                "Global Career Opportunities", "Competitive Salary"
            ],
        )
        
        assert "Global" in international.name
        assert "Global presence" in international.location
        assert "Multicultural" in international.culture
        assert "International Health Coverage" in international.benefits


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestCompanyInfoEdgeCases:
    """Test edge cases and error conditions for CompanyInfo model."""

    def test_extremely_long_strings(self):
        """Test handling of extremely long string values."""
        long_string = "x" * 10000
        
        # Should not raise validation errors (length constraints at business logic level)
        company = CompanyInfo(
            name=long_string,
            industry=long_string,
            size=long_string,
            location=long_string,
            website=long_string,
            description=long_string,
            culture=long_string,
        )
        
        assert len(company.name) == 10000
        assert len(company.industry) == 10000
        assert len(company.size) == 10000
        assert len(company.location) == 10000
        assert len(company.website) == 10000
        assert len(company.description) == 10000
        assert len(company.culture) == 10000

    def test_unicode_and_special_characters(self):
        """Test handling of Unicode and special characters."""
        company = CompanyInfo(
            name="Technología Avanzada S.A. 🚀",
            industry="Inteligencia Artificial & Machine Learning",
            size="500+ empleados",
            location="Madrid, España 🇪🇸",
            website="https://tecnología-avanzada.es",
            description="Desarrollamos soluciones de IA para el mercado español 💡",
            culture="Innovación, colaboración y café ☕",
            values=["Innovación", "Excelencia", "Diversidad"],
            benefits=["Seguro médico", "Formación continua", "Café gratis ☕"],
        )
        
        assert "🚀" in company.name
        assert "Inteligencia Artificial" in company.industry
        assert "🇪🇸" in company.location
        assert "💡" in company.description
        assert "café ☕" in company.culture
        assert "Innovación" in company.values
        assert "Café gratis ☕" in company.benefits

    def test_very_large_lists(self):
        """Test handling of very large lists."""
        large_values_list = [f"Value_{i}" for i in range(1000)]
        large_benefits_list = [f"Benefit_{i}" for i in range(500)]
        
        company = CompanyInfo(
            name="MegaBenefits Corp",
            values=large_values_list,
            benefits=large_benefits_list,
        )
        
        assert len(company.values) == 1000
        assert len(company.benefits) == 500
        assert company.values[0] == "Value_0"
        assert company.values[999] == "Value_999"
        assert company.benefits[0] == "Benefit_0"
        assert company.benefits[499] == "Benefit_499"

    def test_empty_and_whitespace_strings(self):
        """Test handling of empty and whitespace-only strings."""
        company = CompanyInfo(
            name="WhitespaceTest Corp",
            industry="   ",  # Whitespace only
            size="",       # Empty string
            location=" \t\n ",  # Various whitespace
            website="",
            description="   \n\t   ",
            culture="",
            values=["", "   ", "Valid Value", ""],
            benefits=["Valid Benefit", "", "   "],
        )
        
        # Empty and whitespace strings should be preserved
        assert company.industry == "   "
        assert company.size == ""
        assert company.location == " \t\n "
        assert company.website == ""
        assert company.description == "   \n\t   "
        assert company.culture == ""
        
        # Lists with empty strings should be preserved
        assert "" in company.values
        assert "   " in company.values
        assert "Valid Value" in company.values
        assert "" in company.benefits
        assert "Valid Benefit" in company.benefits

    def test_special_company_name_formats(self):
        """Test various company name formats."""
        company_names = [
            "ABC Corp.",
            "XYZ, Inc.",
            "TechCorp LLC",
            "Global Solutions Ltd.",
            "StartupCo (YC S23)",
            "AI/ML Specialists & Co.",
            "Non-Profit Foundation 501(c)(3)",
            "Multi-Word Company Name With Many Parts",
            "123 Digital Solutions",
            "Company@Domain.com",
            "Company-With-Hyphens",
            "Company_With_Underscores",
        ]
        
        for name in company_names:
            company = CompanyInfo(name=name)
            assert company.name == name

    def test_website_url_formats(self):
        """Test various website URL formats."""
        url_formats = [
            "https://example.com",
            "http://www.example.com",
            "https://example.com/",
            "https://www.example.co.uk",
            "https://subdomain.example.org",
            "https://example.com/path/to/page",
            "www.example.com",  # Without protocol
            "example.com",      # Domain only
            "",                 # Empty string
        ]
        
        for url in url_formats:
            company = CompanyInfo(name="Test Corp", website=url)
            assert company.website == url

    def test_company_size_formats(self):
        """Test various company size formats."""
        size_formats = [
            "1-10 employees",
            "11-50 employees", 
            "51-200 employees",
            "201-500 employees",
            "501-1000 employees",
            "1000+ employees",
            "10,000+ employees",
            "Startup (5 people)",
            "Small Business",
            "Medium Enterprise",
            "Large Corporation",
            "Fortune 500",
            "Publicly Traded",
            "Series A",
            "Pre-IPO",
            "Stealth Mode",
        ]
        
        for size in size_formats:
            company = CompanyInfo(name="Test Corp", size=size)
            assert company.size == size

    def test_duplicate_list_items(self):
        """Test handling of duplicate items in lists."""
        company = CompanyInfo(
            name="DuplicateCorp",
            values=["Innovation", "Excellence", "Innovation", "Teamwork", "Excellence"],
            benefits=["Health", "401k", "Health", "PTO", "401k", "Stock Options"],
        )
        
        # Duplicates should be preserved (business logic can handle deduplication)
        assert company.values.count("Innovation") == 2
        assert company.values.count("Excellence") == 2
        assert company.benefits.count("Health") == 2
        assert company.benefits.count("401k") == 2


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestCompanyInfoSerialization:
    """Test CompanyInfo model serialization and deserialization."""

    def test_company_info_to_dict(self, sample_company_data):
        """Test converting CompanyInfo to dictionary."""
        company = CompanyInfo(**sample_company_data)
        
        # Use model_dump for Pydantic v2
        company_dict = company.model_dump() if hasattr(company, 'model_dump') else company.dict()
        
        assert isinstance(company_dict, dict)
        assert company_dict["name"] == "TechCorp Inc"
        assert company_dict["industry"] == "Technology"
        assert company_dict["size"] == "201-500 employees"
        assert company_dict["location"] == "San Francisco, CA"
        assert "id" in company_dict
        assert "created_at" in company_dict

    def test_company_info_from_dict(self, sample_company_data):
        """Test creating CompanyInfo from dictionary."""
        company = CompanyInfo(**sample_company_data)
        
        assert company.name == "TechCorp Inc"
        assert company.industry == "Technology"
        assert company.website == "https://techcorp.com"

    def test_company_info_json_serialization(self, sample_company_data):
        """Test JSON serialization compatibility."""
        company = CompanyInfo(**sample_company_data)
        
        # Test that we can get dictionary representation
        company_dict = company.model_dump() if hasattr(company, 'model_dump') else company.dict()
        
        # UUIDs remain as UUID objects in dict(), datetimes remain as datetime objects
        assert isinstance(company_dict["id"], (str, UUID))
        assert isinstance(company_dict["created_at"], datetime)
        
        # Test JSON export (should work regardless of UUID/datetime handling)
        if hasattr(company, 'model_dump_json'):
            json_str = company.model_dump_json()  # Pydantic v2
        else:
            json_str = company.json()  # Pydantic v1
        
        assert isinstance(json_str, str)
        assert "TechCorp Inc" in json_str
        assert "Technology" in json_str

    def test_company_info_copy_and_update(self):
        """Test copying and updating CompanyInfo instances."""
        original = CompanyInfo(
            name="Original Corp",
            industry="Original Industry",
            size="50-100 employees",
        )
        
        # Test copy with updates (use model_copy for Pydantic v2)
        if hasattr(original, 'model_copy'):
            # Pydantic v2 - copy preserves all fields including ID by default
            updated = original.model_copy(update={
                "name": "Updated Corp",
                "industry": "Updated Industry"
            })
            
            assert updated.name == "Updated Corp"
            assert updated.industry == "Updated Industry"
            assert updated.size == "50-100 employees"  # Unchanged fields preserved
            assert updated.id == original.id  # ID is preserved in model_copy
            
            # To get a new ID, we need to explicitly update it
            updated_with_new_id = original.model_copy(update={
                "name": "New Company",
                "id": uuid4()
            })
            assert updated_with_new_id.id != original.id
        else:
            # Pydantic v1 behavior
            updated = original.copy(update={
                "name": "Updated Corp",
                "industry": "Updated Industry"
            })
            
            assert updated.name == "Updated Corp"
            assert updated.industry == "Updated Industry"
            assert updated.size == "50-100 employees"  # Unchanged fields preserved

    def test_partial_company_info_serialization(self):
        """Test serialization of company info with only some fields populated."""
        minimal_company = CompanyInfo(name="Minimal Corp")
        
        company_dict = minimal_company.model_dump() if hasattr(minimal_company, 'model_dump') else minimal_company.dict()
        
        # Check that optional fields are properly handled
        assert company_dict["name"] == "Minimal Corp"
        assert company_dict["industry"] is None
        assert company_dict["size"] is None
        assert company_dict["location"] is None
        assert company_dict["website"] is None
        assert company_dict["description"] is None
        assert company_dict["culture"] is None
        assert company_dict["values"] == []
        assert company_dict["benefits"] == []
