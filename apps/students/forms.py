from django import forms

from apps.accounts.models import User
from .models import StudentProfile


class StudentContactForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone", "date_of_birth"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class StudentAcademicProfileForm(forms.ModelForm):
    def __init__(self, *args, catalog, **kwargs):
        super().__init__(*args, **kwargs)
        self.catalog = catalog
        self.fields["other_institution"] = forms.CharField(required=False, label="Institution name")
        self.fields["other_faculty_name"] = forms.CharField(required=False, label="Faculty name")
        self.fields["other_department"] = forms.CharField(required=False, label="Department name")
        for field_name in ("institution", "faculty_name", "academic_department"):
            self.fields[field_name].widget = forms.Select()
        universities = catalog["universities"]

        institution_choices = [("", "Choose an institution")]
        institution_choices.extend((university["name"], university["name"]) for university in universities)
        institution_choices.append(("__other__", "Other Nigerian institution (enter name)"))
        known_institutions = {name for name, _label in institution_choices}
        institution_is_other = bool(self.instance.institution and self.instance.institution not in known_institutions)
        if institution_is_other:
            institution_choices.append((self.instance.institution, self.instance.institution))
        self.fields["institution"].choices = institution_choices

        if not self.is_bound and institution_is_other:
            self.initial["institution"] = "__other__"
            self.initial["other_institution"] = self.instance.institution
        selected_institution = (
            self.data.get(self.add_prefix("institution"))
            if self.is_bound else self.initial.get("institution", self.instance.institution)
        )
        university = next((u for u in universities if u["name"] == selected_institution), None)
        faculties = university["faculties"] if university else []
        faculty_choices = [("", "Choose a faculty")] + [
            (faculty["name"], faculty["name"]) for faculty in faculties
        ]
        faculty_choices.append(("__other__", "Other faculty (enter name)"))
        known_faculties = {name for name, _label in faculty_choices}
        faculty_is_other = bool(self.instance.faculty_name and self.instance.faculty_name not in known_faculties)
        if faculty_is_other:
            faculty_choices.append((self.instance.faculty_name, self.instance.faculty_name))
            if not self.is_bound:
                self.initial["faculty_name"] = "__other__"
                self.initial["other_faculty_name"] = self.instance.faculty_name
        self.fields["faculty_name"].choices = faculty_choices
        selected_faculty = (
            self.data.get(self.add_prefix("faculty_name"))
            if self.is_bound else self.initial.get("faculty_name", self.instance.faculty_name)
        )
        faculty = next((f for f in faculties if f["name"] == selected_faculty), None)
        departments = faculty["departments"] if faculty else []
        department_choices = [("", "Choose a department")] + [
            (department, department) for department in departments
        ]
        department_choices.append(("__other__", "Other department (enter name)"))
        known_departments = {name for name, _label in department_choices}
        department_is_other = bool(self.instance.academic_department and self.instance.academic_department not in known_departments)
        if department_is_other:
            department_choices.append((self.instance.academic_department, self.instance.academic_department))
            if not self.is_bound:
                self.initial["academic_department"] = "__other__"
                self.initial["other_department"] = self.instance.academic_department
        self.fields["academic_department"].choices = department_choices
        for field_name in ("institution", "faculty_name", "academic_department"):
            self.fields[field_name].widget.choices = self.fields[field_name].choices

        self.fields["institution"].label = "Institution / university"
        self.fields["faculty_name"].label = "Faculty"
        self.fields["academic_department"].label = "Department"

    def clean_student_id(self):
        return self.cleaned_data["student_id"] or None

    def clean_institution(self):
        value = self.cleaned_data["institution"]
        if value == "__other__":
            value = self.data.get(self.add_prefix("other_institution"), "").strip()
            if not value:
                raise forms.ValidationError("Enter your institution name.")
        return value

    def clean_faculty_name(self):
        value = self.cleaned_data["faculty_name"]
        if value == "__other__":
            value = self.data.get(self.add_prefix("other_faculty_name"), "").strip()
            if not value:
                raise forms.ValidationError("Enter your faculty name.")
        return value

    def clean_academic_department(self):
        value = self.cleaned_data["academic_department"]
        if value == "__other__":
            value = self.data.get(self.add_prefix("other_department"), "").strip()
            if not value:
                raise forms.ValidationError("Enter your department name.")
        return value

    class Meta:
        model = StudentProfile
        fields = ["student_id", "institution", "faculty_name", "academic_department", "level", "sex"]
