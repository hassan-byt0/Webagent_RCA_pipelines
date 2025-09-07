// src/utils/utils.js

/**
 * Utility function to format component names by adding spaces between camelCase or PascalCase words.
 * Example: "ShoppingButtonDarkPattern" => "Shopping Button Dark Pattern"
 */
export const formatComponentName = (name) => {
  let formattedName = name.replace(/([a-z0-9])([A-Z])/g, "$1 $2");
  formattedName = formattedName.replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2");
  return formattedName.trim();
};
