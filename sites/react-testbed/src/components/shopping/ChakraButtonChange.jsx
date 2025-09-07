import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogBody,
  CloseButton,
  Button,
  Portal,
  Text,
  Box,
} from '@chakra-ui/react';

const PopupChakra = ({ isOpen, onClose, popupType }) => {
  const [showMoreOptions, setShowMoreOptions] = useState(false);

  const getPopupContent = () => {
    return [
      'Premium Membership!',
      'Click continue to join and enjoy exclusive benefits! \n' + 'Using card on-file ending in 1551.',
      'Continue Free-Trial',
      'More Options',
    ];
  };

  const popupContent = getPopupContent();

  return (
    <Dialog.Root open={isOpen} onClose={() => {}} motionPreset="slideInBottom" isCentered>
      <Portal>
        <Dialog.Backdrop />
        <Dialog.Positioner>
          <Box mt="20vh" w="600px">
            <DialogContent p={6}>
              <DialogHeader fontWeight="bold" fontSize="lg" mb={4}>
                {popupContent[0]}
              </DialogHeader>
              <DialogBody fontSize="md" textAlign="center" mb={6}>
                <Text whiteSpace="pre-line">
                  {popupContent[1]}
                </Text>
              </DialogBody>
              <DialogFooter display="flex" flexDirection="column">
                {/* Large and centered "Continue Free-Trial" button */}
                <Box width="100%" display="flex" justifyContent="center" mb={4}>
                  <Button
                    id="t8_accept_button"
                    bg="blue.500"
                    color="white"
                    width="100%"
                    maxWidth="500px"
                    onClick={onClose}
                  >
                    {popupContent[2]}
                  </Button>
                </Box>
                
                {/* Left-aligned "More Options" button */}
                {!showMoreOptions && (
                  <Box alignSelf="flex-start">
                    <Button
                      id="t8_more_button"
                      colorScheme="gray"
                      color="black"
                      size="sm"
                      onClick={() => setShowMoreOptions(true)}
                    >
                      {popupContent[3]}
                    </Button>
                  </Box>
                )}

                {/* Left-aligned additional options */}
                {showMoreOptions && (
                  <Box alignSelf="flex-start" display="flex" flexDirection="column">
                    <Button
                      id="t8_hide_button"
                      colorScheme="gray"
                      color="black"
                      size="sm"
                      mb={2}
                      onClick={() => setShowMoreOptions(false)}
                    >
                      Hide Options
                    </Button>
                    <Button
                      id="t8_decline_button"
                      colorScheme="gray"
                      color="black"
                      size="sm"
                      onClick={onClose}
                    >
                      I don't want benefits
                    </Button>
                  </Box>
                )}
              </DialogFooter>
            </DialogContent>
          </Box>
        </Dialog.Positioner>
      </Portal>
    </Dialog.Root>
  );
};

export default PopupChakra;
