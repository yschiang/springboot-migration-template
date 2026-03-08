# Scanned Files — cline-springboot-migration-demo

| Field | Value |
|---|---|
| **Date** | `2026-03-08` |
| **Total Files** | `30` |
| **Type Counts** | `Java: 27, Config: 2, Build: 1` |

## Directory Structure

```
cline-springboot-migration-demo/
  src/
    main/
      java/
        org/
          springframework/
            samples/
              petclinic/
                PetClinicApplication.java        ⚠ C10
                config/
                  AppProperties.java             ⚠ W6
                  BatchConfig.java              ⚠ C11, W4, W5
                  RestTemplateConfig.java       ⚠ C9
                  SecurityConfig.java           ⚠ C6, C7, C8, W8
                model/
                  BaseEntity.java               ⚠ C2
                  NamedEntity.java              ⚠ C2, C3
                  Person.java                   ⚠ C2, C3
                owner/
                  Owner.java                    ⚠ C2, C3
                  OwnerController.java          ⚠ C3, C5, C8
                  OwnerRepository.java
                  Pet.java                      ⚠ C2
                  PetController.java            ⚠ C3
                  PetType.java                  ⚠ C2
                  PetTypeRepository.java
                  PetValidator.java
                  Visit.java                    ⚠ C2, C3
                  VisitController.java          ⚠ C3
                system/
                  CacheConfiguration.java
                  CrashController.java
                  WelcomeController.java
                vet/
                  Specialty.java                ⚠ C2
                  Vet.java                      ⚠ C2, C4
                  VetController.java            ⚠ C8
                  VetRepository.java
                  Vets.java                     ⚠ C4
      resources/
        application-mysql.properties
        application.properties                 ⚠ C14, W1, W2, W3, W5
    test/
      java/
        org/
          springframework/
            samples/
              petclinic/
                PetClinicIntegrationTests.java
  pom.xml                                      ⚠ C1, C4, C9, C10, C12, C13, W7  💡 S1
```

## Files Read

| # | File | Type | Size |
|---|------|------|------|
| 1 | `pom.xml` | Build | `190 lines` |
| 2 | `src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java` | Java | `15 lines` |
| 3 | `src/main/java/org/springframework/samples/petclinic/config/AppProperties.java` | Java | `33 lines` |
| 4 | `src/main/java/org/springframework/samples/petclinic/config/BatchConfig.java` | Java | `56 lines` |
| 5 | `src/main/java/org/springframework/samples/petclinic/config/RestTemplateConfig.java` | Java | `30 lines` |
| 6 | `src/main/java/org/springframework/samples/petclinic/config/SecurityConfig.java` | Java | `32 lines` |
| 7 | `src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java` | Java | `28 lines` |
| 8 | `src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java` | Java | `27 lines` |
| 9 | `src/main/java/org/springframework/samples/petclinic/model/Person.java` | Java | `32 lines` |
| 10 | `src/main/java/org/springframework/samples/petclinic/owner/Owner.java` | Java | `119 lines` |
| 11 | `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java` | Java | `171 lines` |
| 12 | `src/main/java/org/springframework/samples/petclinic/owner/OwnerRepository.java` | Java | `13 lines` |
| 13 | `src/main/java/org/springframework/samples/petclinic/owner/Pet.java` | Java | `59 lines` |
| 14 | `src/main/java/org/springframework/samples/petclinic/owner/PetController.java` | Java | `122 lines` |
| 15 | `src/main/java/org/springframework/samples/petclinic/owner/PetType.java` | Java | `12 lines` |
| 16 | `src/main/java/org/springframework/samples/petclinic/owner/PetTypeRepository.java` | Java | `13 lines` |
| 17 | `src/main/java/org/springframework/samples/petclinic/owner/PetValidator.java` | Java | `29 lines` |
| 18 | `src/main/java/org/springframework/samples/petclinic/owner/Visit.java` | Java | `40 lines` |
| 19 | `src/main/java/org/springframework/samples/petclinic/owner/VisitController.java` | Java | `68 lines` |
| 20 | `src/main/java/org/springframework/samples/petclinic/system/CacheConfiguration.java` | Java | `23 lines` |
| 21 | `src/main/java/org/springframework/samples/petclinic/system/CrashController.java` | Java | `14 lines` |
| 22 | `src/main/java/org/springframework/samples/petclinic/system/WelcomeController.java` | Java | `13 lines` |
| 23 | `src/main/java/org/springframework/samples/petclinic/vet/Specialty.java` | Java | `12 lines` |
| 24 | `src/main/java/org/springframework/samples/petclinic/vet/Vet.java` | Java | `53 lines` |
| 25 | `src/main/java/org/springframework/samples/petclinic/vet/VetController.java` | Java | `50 lines` |
| 26 | `src/main/java/org/springframework/samples/petclinic/vet/VetRepository.java` | Java | `19 lines` |
| 27 | `src/main/java/org/springframework/samples/petclinic/vet/Vets.java` | Java | `21 lines` |
| 28 | `src/main/resources/application-mysql.properties` | Config | `7 lines` |
| 29 | `src/main/resources/application.properties` | Config | `38 lines` |
| 30 | `src/test/java/org/springframework/samples/petclinic/PetClinicIntegrationTests.java` | Java | `14 lines` |
