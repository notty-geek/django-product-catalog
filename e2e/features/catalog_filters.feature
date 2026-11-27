Feature: Find products in the sample catalog
  Background:
    Given I open the product catalog

  Scenario: Search for part of a description regardless of case or surrounding spaces
    When I enter "  SH cOnE  " in the description search
    And I apply the filters
    Then I see exactly these products
      | Product               |
      | Pour-over Coffee Cone |

  Scenario: Browse one category
    When I choose the "Outdoors" category
    And I apply the filters
    Then I see exactly these products
      | Product               |
      | Folding Camp Stool    |
      | Picnic Blanket        |
      | Pocket Trail Map Case |
      | Trail Coffee Flask    |

  Scenario: Require every selected tag
    When I select the "Stainless steel" tag
    And I select the "Reusable" tag
    And I apply the filters
    Then I see exactly these products
      | Product               |
      | Pour-over Coffee Cone |
      | Trail Coffee Flask    |

  Scenario: Combine a description, a category, and multiple tags
    When I enter "coffee" in the description search
    And I choose the "Outdoors" category
    And I select the "Insulated" tag
    And I select the "Stainless steel" tag
    And I apply the filters
    Then I see exactly these products
      | Product            |
      | Trail Coffee Flask |
